from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from kontext_copilot.copilot import Planner
from kontext_copilot.data.schemas import (
    SessionInitRequestModel,
    SessionInitResponseModel,
    RunSqlRequestModel,
    MessageModel,
    Message,
    ChatRoles,
)
from kontext_copilot.utils import get_logger

router = APIRouter(
    tags=["copilot"],
    prefix="/api/copilot",
    responses={
        404: {"description": "Not found"},
    },
)

logger = get_logger()


def _get_planner(
    model: str,
    data_source_id: int,
    tables: Optional[list[str]] = None,
    schema: Optional[str] = None,
    session_id: Optional[int] = None,
):
    """
    Get planner
    """
    planner = Planner()
    planner.init_session(
        model=model,
        data_source_id=data_source_id,
        tables=tables,
        schema=schema,
        session_id=session_id,
    )
    return planner


@router.post("/init_session", response_model=SessionInitResponseModel)
def init_session(
    request: SessionInitRequestModel = Body(None),
) -> SessionInitResponseModel:
    """
    Init session with system prompt
    """
    logger.debug("Request: %s", request)
    planner = _get_planner(
        model=request.model,
        data_source_id=request.data_source_id,
        tables=request.tables,
        schema=request.schema_name,
        session_id=request.session_id,
    )

    prompt = planner.get_system_prompt()

    logger.debug("System prompt: %s", prompt)

    session = planner.get_session_model()
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
    planner = _get_planner(
        model="copilot",
        data_source_id=request.data_source_id,
        schema=request.schema_name,
    )
    response = planner.run_sql(
        sql=request.sql,
        max_records=request.max_records,
    )

    def generate_response():
        for res in response:
            message = MessageModel(
                message=Message(role=ChatRoles.ASSISTANT, content=res),
                model="copilot",
                created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                done=False,
            )
            yield message.model_dump_json() + "\n"

        # Return a message to indicate the SQL execution is done
        yield MessageModel(
            message=Message(role=ChatRoles.SYSTEM, content=""),
            model="copilot",
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            done=True,
        ).model_dump_json() + "\n"

    return StreamingResponse(generate_response(), media_type="application/x-ndjson")
