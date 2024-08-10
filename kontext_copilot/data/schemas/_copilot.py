from typing import Optional
from kontext_copilot.data.schemas._common import CamelAliasBaseModel


class CopilotSessionRequestModel(CamelAliasBaseModel):
    model: str
    data_source_id: int
    tables: Optional[list[str]] = None
    schema_name: Optional[str] = None


class CopilotSessionResponseModel(CamelAliasBaseModel):
    prompt: str


class CopilotRunSqlRequestModel(CamelAliasBaseModel):
    data_source_id: int
    sql: str
    schema_name: Optional[str] = None
    max_records: Optional[int] = 10
