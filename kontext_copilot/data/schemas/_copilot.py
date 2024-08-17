import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import field_validator

from kontext_copilot.data.schemas._common import CamelAliasBaseModel
from kontext_copilot.data.schemas._llm import LlmChatMessage
from kontext_copilot.ollama._types import Options


class ActionTypes(str, Enum):
    RUN_SQL = "run_sql"
    SQL_TO_PYTHON = "sql_to_python"
    SQL_TO_PYSPARK = "sql_to_pyspark"


class ActionModel(CamelAliasBaseModel):
    action: ActionTypes
    data: Optional[Dict[str, Any]] = None


class RunSqlRequestModel(CamelAliasBaseModel):
    data_source_id: int
    sql: str
    schema_name: Optional[str] = None
    max_records: Optional[int] = 10
    session_id: Optional[int] = None


class SessionInitRequestModel(CamelAliasBaseModel):
    model: str
    data_source_id: Optional[int] = None
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
    data_source_id: Optional[int] = None


class SessionUpdateModel(CamelAliasBaseModel):
    data_source_id: Optional[int] = None
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
    data_source_id: Optional[int] = None
    tables: Optional[list[str]] = None
    schema_name: Optional[str] = None
    system_prompt: Optional[str] = None
    title: Optional[str] = None
    created_at: datetime

    def model_dump(
        self,
        **kwargs,
    ):
        data = super().model_dump(**kwargs)
        if isinstance(data["tables"], list):
            data["tables"] = ",".join(data["tables"])
        return data


class SessionMessageModel(LlmChatMessage):
    id: Optional[int] = None
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
    actions: Optional[List[ActionModel]] = None
    created_at: Optional[datetime] = datetime.now()

    # Convert actions from JSON str to list of ActionModel
    @field_validator("actions", mode="before")
    def convert_actions(cls, value):
        if value is None:
            return []
        # if it is a string, convert to list of action model from JSON
        if isinstance(value, str):
            return [ActionModel(**action) for action in json.loads(value)]
        else:
            return value


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
    actions: Optional[List[ActionModel]] = None


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
    actions: Optional[List[ActionModel]] = None

    def model_dump(
        self,
        **kwargs,
    ):
        data = super().model_dump(**kwargs)
        if isinstance(data["actions"], list):
            # Convert to json string
            data["actions"] = json.dumps(data["actions"])
        return data


class ChatRequestModel(CamelAliasBaseModel):
    model: str
    messages: Optional[list[LlmChatMessage]] = None
    stream: Optional[bool] = False
    format: Literal["", "json"] = ""
    options: Optional[Options] = None
    keep_alive: Optional[Union[float, str]] = None
    session_id: Optional[int] = None


class CodeBlockModel(CamelAliasBaseModel):
    language: Optional[str] = None
    code: str


class EmbeddingsRequestModel(CamelAliasBaseModel):
    model: str
    prompt: str
    keep_alive: Optional[Union[str, int]] = None
    options: Optional[Options] = None


class EmbeddingsResponseModel(CamelAliasBaseModel):
    embedding: List[float]


class GenerateRequestModel(CamelAliasBaseModel):
    model: str
    prompt: str
    suffix: Optional[str] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    stream: Optional[bool] = None
    raw: Optional[bool] = None
    format: Optional[str] = None
    images: Optional[Union[List[bytes], List[str]]] = None
    keep_alive: Optional[Union[str, int]] = None
    options: Optional[Options] = None


class GenerateResponseModel(CamelAliasBaseModel):
    model: str
    created_at: datetime
    response: str
    done: bool
    done_reason: Optional[str] = None
    context: Optional[List[int]] = None
    total_duration: Optional[float] = None
    load_duration: Optional[float] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[float] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[float] = None
