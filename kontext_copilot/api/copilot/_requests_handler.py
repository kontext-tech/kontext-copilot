import json
from typing import Generator, Iterator, Optional

from fastapi import APIRouter, Body, Depends, Response
from fastapi.responses import StreamingResponse

from kontext_copilot import ollama
from kontext_copilot.copilot import CopilotOrchestrator
from kontext_copilot.data.schemas import (
    AddUserMessageRequestModel,
    ChartDataRequestModel,
    ChartDataResponseModel,
    ChatRequestModel,
    EmbeddingsRequestModel,
    EmbeddingsResponseModel,
    GenerateRequestModel,
    GenerateResponseModel,
    LlmModelListResponse,
    RunSqlRequestModel,
    SessionInitRequestModel,
    SessionInitResponseModel,
)
from kontext_copilot.services import SettingsService, get_settings_service
from kontext_copilot.utils import get_logger

router = APIRouter(
    tags=["copilot"],
    prefix="/api/copilot",
    responses={
        404: {"description": "Not found"},
    },
)

logger = get_logger()


def _get_orchestrator(
    model: str,
    data_source_id: Optional[int] = None,
    tables: Optional[list[str]] = None,
    schema: Optional[str] = None,
    session_id: Optional[int] = None,
):
    """
    Get orchestrator
    """
    orchestrator = CopilotOrchestrator()
    orchestrator.init_session(
        model,
        data_source_id,
        tables=tables,
        schema=schema,
        session_id=session_id,
    )
    return orchestrator


@router.post("/init-session", response_model=SessionInitResponseModel)
def init_session(
    request: SessionInitRequestModel = Body(None),
) -> SessionInitResponseModel:
    """
    Init session with system prompt
    """
    logger.debug("Request: %s", request)
    orchestrator = _get_orchestrator(
        model=request.model,
        data_source_id=request.data_source_id,
        tables=request.tables,
        schema=request.schema_name,
        session_id=request.session_id,
    )

    prompt = orchestrator.get_system_prompt()

    logger.debug("System prompt: %s", prompt)

    session = orchestrator.get_session_model()
    return SessionInitResponseModel(
        system_prompt=prompt,
        session_id=session.id,
        title=session.title,
        schema_name=session.schema_name,
        tables=session.tables,
        model=session.model,
        data_source_id=session.data_source_id,
    )


@router.post("/run-sql")
def run_sql(request: RunSqlRequestModel = Body(None)):
    """
    Run SQL
    """
    orchestrator = _get_orchestrator(
        model="copilot",
        data_source_id=request.data_source_id,
        schema=request.schema_name,
        session_id=request.session_id,
    )
    return StreamingResponse(
        orchestrator.run_sql(request=request), media_type="application/x-ndjson"
    )


@router.post("/chat")
async def chat(
    request: ChatRequestModel, settings: SettingsService = Depends(get_settings_service)
):
    """
    Run SQL
    """
    logger.info("Chat API invoked: %s", request)

    orchestrator = _get_orchestrator(
        model=request.model,
        session_id=request.session_id,
    )

    chat_response = orchestrator.chat(
        settings.get_settings_obj().llm_ollama_endpoint, request=request
    )

    if isinstance(chat_response, Generator):
        return StreamingResponse(chat_response, media_type="application/x-ndjson")
    else:
        return Response(chat_response)


def _get_client(settings_service: SettingsService) -> ollama.Client:
    settings = settings_service.get_settings_obj()
    return ollama.Client(
        host=settings.llm_ollama_endpoint,
    )


@router.get("/tags")
def list_models(
    settings_service: SettingsService = Depends(get_settings_service),
) -> LlmModelListResponse:
    """
    Get a list of available models.
    """
    logger.info("Getting list of models")
    response = _get_client(settings_service=settings_service).list()
    return response


@router.post("/generate")
async def generate(
    request: GenerateRequestModel = Body(None),
    settings_service: SettingsService = Depends(get_settings_service),
):
    logger.debug("Generate API invoked: %s", request)

    client = _get_client(settings_service=settings_service)
    response = client.generate(**request.model_dump(exclude_unset=True))

    # Always return as streaming
    if isinstance(response, Iterator):

        def generate_response():
            for res in iter(response):
                yield GenerateResponseModel(**res).model_dump_json(
                    exclude_unset=True
                ) + "\n"

        return StreamingResponse(generate_response(), media_type="application/x-ndjson")

    if response is not None:
        return Response(
            GenerateResponseModel(**response).model_dump_json(by_alias=True)
        )


@router.post("/embeddings")
async def generate_embeddings(
    request: EmbeddingsRequestModel = Body(None),
    settings_service: SettingsService = Depends(get_settings_service),
):
    logger.debug("Embeddings API invoked: %s", request)

    client = _get_client(settings_service=settings_service)
    response = client.embeddings(**request.model_dump(exclude_unset=True))
    reseponse_model = EmbeddingsResponseModel(**response)
    return Response(reseponse_model.model_dump_json(by_alias=True))


@router.post("/add-user-message")
async def add_user_message(request: AddUserMessageRequestModel = Body(None)):
    logger.debug("Add User Message API invoked: %s", request)

    planner = _get_orchestrator(
        model=request.model,
        session_id=request.session_id,
    )

    return Response(
        planner.session.add_user_message(request.content).model_dump_json(by_alias=True)
    )


# endpoint to get chart data
@router.post("/get-chart-data")
async def get_chart_data(
    request: ChartDataRequestModel = Body(None),
) -> ChartDataResponseModel:
    """
    Get chart data
    """
    orchestrator = _get_orchestrator(
        model="copilot",
        data_source_id=request.data_source_id,
        schema=request.schema_name,
        session_id=request.session_id,
    )
    return orchestrator.get_chart_data(request=request)
