from fastapi import APIRouter, Body
from kontext_copilot.copilot import Planner
from kontext_copilot.data.schemas import (
    CopilotSessionRequestModel,
    CopilotSessionResponseModel,
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


@router.post("/session", response_model=CopilotSessionResponseModel)
def get_system_prompt(
    request: CopilotSessionRequestModel = Body(None),
) -> CopilotSessionResponseModel:
    """
    Get system prompt
    """
    logger.debug("Request: %s", request)
    planner = Planner()
    planner.init_session(
        data_source_id=request.get("data_source_id"),
        tables=request.get("tables"),
        schema=request.get("schema"),
    )

    prompt = planner.get_system_prompt()

    logger.debug("System prompt: %s", prompt)

    return CopilotSessionResponseModel(prompt=prompt)
