import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import Field, field_validator

from kontext_copilot.data.schemas._common import CamelAliasBaseModel
from kontext_copilot.data.schemas._llm import LlmChatMessage
from kontext_copilot.ollama._types import Options


class ActionTypes(str, Enum):
    RUN_SQL = "run_sql"
    COPY_SQL = "copy_sql"
    SQL_TO_PYTHON = "sql_to_python"
    SQL_TO_PYSPARK = "sql_to_pyspark"
    FIX_SQL_ERRORS = "fix_sql_errors"
    RECOMMEND_CHARTS = "recommend_charts"


class ActionsModel(CamelAliasBaseModel):
    actions: List[ActionTypes]
    data: Optional[Dict[str, Any]] = None


class ActionsDataKeys(str, Enum):
    SQL_LIST = "sql"
    SQL_TEXT = "sqlText"
    SQL_TO_PYTHON_PROMPT = "sqlToPythonPrompt"
    SQL_TO_PYSPARK_PROMPT = "sqlToPysparkPrompt"
    FIX_SQL_ERRORS_PROMPT = "fixSqlErrorsPrompt"
    RECOMMENDED_CHARTS = "recommendedCharts"


class RunSqlRequestModel(CamelAliasBaseModel):
    data_source_id: int
    sql: str
    schema_name: Optional[str] = None
    max_records: Optional[int] = 10
    session_id: Optional[int] = None
    parent_message_id: Optional[int] = None


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
    actions: Optional[ActionsModel] = None
    created_at: Optional[datetime] = datetime.now()

    # Convert actions from JSON str to ActionsModel
    @field_validator("actions", mode="before")
    def convert_actions(cls, value):
        if value is None:
            return ActionsModel(actions=[], data={})
        # if it is a string, convert to list of action model from JSON
        if isinstance(value, str):
            return ActionsModel(**json.loads(value))
        else:
            return value

    def init_actions(self):
        if self.actions is None:
            self.actions = ActionsModel(actions=[], data={})

    def add_actions(
        self,
        actions: List[ActionTypes],
        data: Optional[Dict[str, Any]] = None,
    ):
        self.init_actions()
        self.actions.actions.extend(actions)

        if data is not None:
            for key, value in data.items():
                if key in self.actions.data:
                    if isinstance(self.actions.data[key], list):
                        self.actions.data[key].append(value)
                    else:
                        self.actions.data[key] = value
                else:
                    self.actions.data[key] = value


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
    actions: Optional[ActionsModel] = None


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
    actions: Optional[ActionsModel] = None

    def model_dump(
        self,
        **kwargs,
    ):
        data = super().model_dump(**kwargs)
        if isinstance(data["actions"], dict):
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


class AddUserMessageRequestModel(CamelAliasBaseModel):
    session_id: Optional[int] = None
    content: str
    model: str


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


class ColumnStatsModel(CamelAliasBaseModel):
    column_name: str
    column_type: str
    min_val: Any
    max_val: Any
    approx_unique: int
    avg: Optional[float] = None
    std: Optional[float] = None
    q25: Optional[float] = None
    q50: Optional[float] = None
    q75: Optional[float] = None
    count: int
    null_percentage: float


class QueryStatsModel(CamelAliasBaseModel):
    cache_table_name: str
    cached: bool = False
    column_stats: List[ColumnStatsModel]
    categorical_columns: Optional[List[str]] = None
    datetime_columns: Optional[List[str]] = None
    numerical_columns: Optional[List[str]] = None
    boolean_columns: Optional[List[str]] = None


class ChartTypes(str, Enum):
    PIE = "pie"
    BAR = "bar"
    LINE = "line"


class AggregateTypes(str, Enum):
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MAX = "max"
    MIN = "min"


class ChartModel(CamelAliasBaseModel):
    chart_type: ChartTypes
    aggregate_type: Optional[AggregateTypes] = None


class PieChartModel(ChartModel):
    chart_type: ChartTypes = ChartTypes.PIE
    title: Optional[str] = None
    data_column: str
    label_column: Optional[str] = None


class BarChartModel(ChartModel):
    chart_type: ChartTypes = ChartTypes.BAR
    title: Optional[str] = None
    x_title: Optional[str] = None
    y_title: Optional[str] = None
    x_data_column: str
    x_label_column: Optional[str] = None
    y_data_column: str
    y_label_column: Optional[str] = None


class LineChartModel(ChartModel):
    chart_type: ChartTypes = ChartTypes.LINE
    title: Optional[str] = None
    x_title: Optional[str] = None
    y_title: Optional[str] = None
    x_data_column: str
    x_label_column: Optional[str] = None
    y_data_column: str
    y_label_column: Optional[str] = None


class ChartDataModel(CamelAliasBaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]


class ChartOptionsModel(CamelAliasBaseModel):
    plugins: Optional[Dict[str, Any]] = None


class ChartDataRequestModel(CamelAliasBaseModel):
    chart: Union[PieChartModel, BarChartModel, LineChartModel]
    cached: bool = False
    cached_table_name: Optional[str] = None
    data_source_id: int
    schema_name: Optional[str] = None
    session_id: Optional[int] = None
    message_id: Optional[int] = None


class ChartDataResponseModel(CamelAliasBaseModel):
    data: ChartDataModel
    type: ChartTypes
    options: Optional[ChartOptionsModel] = None


class ChartListModel(CamelAliasBaseModel):
    charts: List[Union[PieChartModel, BarChartModel, LineChartModel]]
    cached: bool = False
    cached_table_name: Optional[str] = None
