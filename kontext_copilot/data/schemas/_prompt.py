import sys
from typing import List, Optional

from pydantic import BaseModel

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict, NotRequired
else:
    from typing import TypedDict, NotRequired


class PromptInfoModel(TypedDict):
    id: str
    name: NotRequired[str]
    system_defined: NotRequired[bool] = False


class PromptModel(PromptInfoModel):
    prompt: Optional[str]
    system_prompt: Optional[str]
    user_input: Optional[str]


class PromptListModel(BaseModel):
    prompts: List[PromptModel]
