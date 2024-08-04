import sys
from typing import Optional

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict, NotRequired
else:
    from typing import TypedDict, NotRequired


class CopilotSessionRequestModel(TypedDict):
    model: str
    data_source_id: int
    tables: NotRequired[list[str]]
    schema: NotRequired[str]


class CopilotSessionResponseModel(TypedDict):
    prompt: str
