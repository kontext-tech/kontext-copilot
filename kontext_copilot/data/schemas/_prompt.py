from typing import List, Optional

from kontext_copilot.data.schemas._common import CamelAliasBaseModel


class PromptInfoModel(CamelAliasBaseModel):
    id: str
    name: Optional[str] = None
    system_defined: Optional[bool] = False


class PromptModel(PromptInfoModel):
    prompt: Optional[str] = None
    system_prompt: Optional[str] = None
    user_input: Optional[str] = None


class PromptListModel(CamelAliasBaseModel):
    prompts: List[PromptModel]
