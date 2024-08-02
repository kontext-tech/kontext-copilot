import json
import os
from typing import List
from fastapi import APIRouter

from kontext_copilot.data.schemas import PromptsModel, PromptInfoModel, PromptModel
from kontext_copilot.utils import get_logger


router = APIRouter(
    tags=["prompts"],
    prefix="/api/prompts",
    responses={404: {"description": "Not found"}},
)


logger = get_logger()

# prompt template file path
PROMPT_TEMPLATE_FILE = "./prompts.json"
abs_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), PROMPT_TEMPLATE_FILE)
)

# Function to load and parse prompts.json into a Prompts object


def load_prompts_from_json() -> PromptsModel:
    """
    Load prompts from a JSON file and return a Prompts object.

    Returns:
        Prompts: A Prompts object containing the loaded prompts.
    """
    with open(abs_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return PromptsModel(**data)


@router.get("/templates")
def get_prompt_templates() -> List[PromptInfoModel]:
    """
    Get a list of available models.
    """
    logger.info("Getting list of prompt templates")

    prompts = load_prompts_from_json()

    # convert Prompts object to list of PromptInfo objects
    return [
        PromptInfoModel(id=prompt.id, name=prompt.name) for prompt in prompts.prompts
    ]


@router.get("/templates/{template_id}")
def get_prompt_template(template_id: str) -> PromptModel:
    """
    Get a prompt template by id.
    """
    logger.info("Getting prompt template by id: %s", id)
    prompts = load_prompts_from_json()

    # find prompt by id
    prompt = next((p for p in prompts.prompts if p.id == template_id), None)

    return prompt
