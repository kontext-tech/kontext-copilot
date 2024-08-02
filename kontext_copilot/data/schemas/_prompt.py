from typing import List, Optional

from pydantic import BaseModel


class PromptInfoModel(BaseModel):
    id: str
    name: str


class PromptModel(PromptInfoModel):
    prompt: str
    system_prompt: Optional[str]
    user_input: str


class PromptsModel(BaseModel):
    prompts: List[PromptModel]
