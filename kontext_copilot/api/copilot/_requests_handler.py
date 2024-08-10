from datetime import datetime
import json
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from kontext_copilot.copilot import Planner
from kontext_copilot.data.schemas import (
    CopilotSessionRequestModel,
    CopilotSessionResponseModel,
    CopilotRunSqlRequestModel,
    MessageModel,
    Message,
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


def _get_planner(data_source_id: int, tables: list[str] = None, schema: str = None):
    """
    Get planner
    """
    planner = Planner()
    planner.init_session(
        data_source_id=data_source_id,
        tables=tables,
        schema=schema,
    )
    return planner


@router.post("/init_session", response_model=CopilotSessionResponseModel)
def init_session(
    request: CopilotSessionRequestModel = Body(None),
) -> CopilotSessionResponseModel:
    """
    Get system prompt
    """
    logger.debug("Request: %s", request)
    planner = _get_planner(
        data_source_id=request.get("data_source_id"),
        tables=request.get("tables"),
        schema=request.get("schema"),
    )

    prompt = planner.get_system_prompt()

    logger.debug("System prompt: %s", prompt)

    return CopilotSessionResponseModel(prompt=prompt)


@router.post("/run-sql")
def run_sql(request: CopilotRunSqlRequestModel = Body(None)):
    """
    Run SQL
    """
    planner = _get_planner(
        data_source_id=request.data_source_id, schema=request.schema_name
    )
    response = planner.run_sql(
        sql=request.sql,
        max_records=request.max_records,
    )

    def generate_response():
        for res in response:
            message = MessageModel(
                message=Message(role="assistant", content=res),
                model="copilot",
                created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                done=False,
            )
            yield json.dumps(message) + "\n"

        # Return a message to indicate the SQL execution is done
        yield json.dumps(
            MessageModel(
                message=Message(role="assistant", content=""),
                model="copilot",
                created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                done=True,
            )
        ) + "\n"

    return StreamingResponse(generate_response(), media_type="application/x-ndjson")
