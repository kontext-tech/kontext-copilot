from typing import List
from fastapi import APIRouter

from kontext_copilot.copilot import pf
from kontext_copilot.data.schemas import PromptInfoModel, PromptModel
from kontext_copilot.utils import get_logger


router = APIRouter(
    tags=["prompts"],
    prefix="/api/prompts",
    responses={404: {"description": "Not found"}},
)


logger = get_logger()


@router.get("/templates")
def get_prompt_templates() -> List[PromptInfoModel]:
    """
    Get a list of available models.
    """
    logger.info("Getting list of prompt templates")

    prompts = pf.load_prompts_from_json()

    # convert Prompts object to list of PromptInfo objects
    # filter out system defined prompts
    return [
        PromptInfoModel(id=prompt.id, name=prompt.name)
        for prompt in prompts.prompts
        if not prompt.system_defined
    ]


@router.get("/templates/{template_id}")
def get_prompt_template(template_id: str) -> PromptModel:
    """
    Get a prompt template by id.
    """
    logger.info("Getting prompt template by id: %s", id)
    return pf.get_prompt_template_by_id(template_id)
