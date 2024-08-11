from datetime import datetime
from typing import Optional
from kontext_copilot.data.models import Session
from kontext_copilot.data.schemas._common import CamelAliasBaseModel


class RunSqlRequestModel(CamelAliasBaseModel):
    data_source_id: int
    sql: str
    schema_name: Optional[str] = None
    max_records: Optional[int] = 10


class SessionInitRequestModel(CamelAliasBaseModel):
    model: str
    data_source_id: int
    tables: Optional[list[str]] = None
    schema_name: Optional[str] = None


class SessionInitResponseModel(CamelAliasBaseModel):
    system_prompt: str
    session_id: int
    title: Optional[str] = None


class SessionModel(CamelAliasBaseModel):
    id: int
    data_source_id: int
    tables: Optional[str] = None
    schema_name: Optional[str] = None
    model: Optional[str] = None
    tables: Optional[str] = None
    title: Optional[str] = None
    system_prompt: Optional[str] = None
    created_at: datetime
    ended_at: Optional[datetime] = None


class CreateSessionModel(CamelAliasBaseModel):
    model: str
    data_source_id: int
    tables: Optional[str] = None
    schema_name: Optional[str] = None
    system_prompt: Optional[str] = None
