from typing import List, Optional

from pydantic import BaseModel


class PromptInfo(BaseModel):
    id: str
    name: str


class Prompt(PromptInfo):
    prompt: str
    system_prompt: Optional[str]
    user_input: str


class Prompts(BaseModel):
    prompts: List[Prompt]
