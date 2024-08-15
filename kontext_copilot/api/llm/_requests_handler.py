import json
from typing import Iterator

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from kontext_copilot import ollama
from kontext_copilot.data.schemas import LlmModelListResponse, SessionMessageModel
from kontext_copilot.services import SettingsService, get_settings_service
from kontext_copilot.utils import get_logger

router = APIRouter(
    tags=["llm"],
    prefix="/llms/api",
    responses={404: {"description": "Not found"}},
)

logger = get_logger()


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
    request: Request, settings_service: SettingsService = Depends(get_settings_service)
):
    params = await request.json()
    logger.debug("Generate API invoked: %s", params)

    client = _get_client(settings_service=settings_service)
    response = client.generate(**params)

    # Always return as streaming
    if isinstance(response, Iterator):

        def generate_response():
            for res in iter(response):
                yield json.dumps(res) + "\n"

        return StreamingResponse(generate_response(), media_type="application/x-ndjson")

    if response is not None:
        return json.dumps(response)


@router.post("/embeddings")
async def generate_embeddings(
    request: Request, settings_service: SettingsService = Depends(get_settings_service)
):
    params = await request.json()
    logger.debug("Embeddings API invoked: %s", params)

    client = _get_client(settings_service=settings_service)
    response = client.embeddings(**params)
    return response
