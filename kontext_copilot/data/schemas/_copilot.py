import sys
from typing import Optional
from pydantic import BaseModel

from kontext_copilot.data.schemas._common import CamelAliasBaseModel

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


class CopilotRunSqlRequestModel(CamelAliasBaseModel):
    data_source_id: int
    sql: str
    schema_name: Optional[str] = None
    max_records: Optional[int] = 10
