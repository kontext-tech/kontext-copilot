from datetime import datetime
from typing import Optional

from pydantic import field_validator
from kontext_copilot.data.schemas._common import CamelAliasBaseModel


class RunSqlRequestModel(CamelAliasBaseModel):
    data_source_id: int
    sql: str
    schema_name: Optional[str] = None
    max_records: Optional[int] = 10
    session_id: Optional[int] = None


class SessionInitRequestModel(CamelAliasBaseModel):
    model: str
    data_source_id: int
    tables: Optional[list[str]] = None
    schema_name: Optional[str] = None
    session_id: Optional[int] = None


class SessionInitResponseModel(CamelAliasBaseModel):
    system_prompt: str
    session_id: int
    title: Optional[str] = None
    schema_name: Optional[str] = None
    tables: Optional[list[str]] = None
    model: Optional[str] = None
    data_source_id: int


class SessionUpdateModel(CamelAliasBaseModel):
    data_source_id: int
    tables: Optional[list[str]] = None
    schema_name: Optional[str] = None
    model: Optional[str] = None
    title: Optional[str] = None
    system_prompt: Optional[str] = None
    ended_at: Optional[datetime] = None

    @field_validator("tables", mode="before")
    def split_tables(cls, value):
        # Check if it is empty string
        if isinstance(value, str) and len(value.strip()) > 0:
            return value.split(",")
        elif isinstance(value, str):
            return []
        else:
            return value

    def model_dump(
        self,
        **kwargs,
    ):
        data = super().model_dump(**kwargs)
        if isinstance(data["tables"], list) and len(data["tables"]) > 0:
            data["tables"] = ",".join(data["tables"])
        elif isinstance(data["tables"], list):
            data["tables"] = None

        return data


class SessionModel(SessionUpdateModel):
    id: int
    created_at: datetime


class CreateSessionModel(CamelAliasBaseModel):
    model: str
    data_source_id: int
    tables: Optional[list[str]] = None
    schema_name: Optional[str] = None
    system_prompt: Optional[str] = None
    title: Optional[str] = None
    created_at: datetime

    def model_dump(self):
        data = super().model_dump()
        if isinstance(data["tables"], list):
            data["tables"] = ",".join(data["tables"])
        return data


class SessionMessageModel(CamelAliasBaseModel):
    id: int
    session_id: int
    content: Optional[str] = None
    role: Optional[str] = None
    model: Optional[str] = None
    parent_message_id: Optional[int]
    done: Optional[bool] = False
    copilot_generated: Optional[bool] = False
    is_system_prompt: Optional[bool] = False
    is_error: Optional[bool] = False
    is_streaming: Optional[bool] = False
    generating: Optional[bool] = False
    actions: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()


class CreateSessionMessageModel(CamelAliasBaseModel):
    session_id: int
    content: Optional[str] = None
    role: Optional[str] = None
    model: Optional[str] = None
    parent_message_id: Optional[int] = None
    done: Optional[bool] = False
    copilot_generated: Optional[bool] = False
    is_system_prompt: Optional[bool] = False
    is_error: Optional[bool] = False
    is_streaming: Optional[bool] = False
    generating: Optional[bool] = False
    actions: Optional[str] = None


class UpdateSessionMessageModel(CamelAliasBaseModel):
    session_id: Optional[int] = None
    content: Optional[str] = None
    role: Optional[str] = None
    model: Optional[str] = None
    parent_message_id: Optional[int] = None
    done: Optional[bool] = False
    copilot_generated: Optional[bool] = False
    is_system_prompt: Optional[bool] = False
    is_error: Optional[bool] = False
    is_streaming: Optional[bool] = False
    generating: Optional[bool] = False
    actions: Optional[str] = None
