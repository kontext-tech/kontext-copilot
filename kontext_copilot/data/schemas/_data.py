from typing import Any, List, Optional

from kontext_copilot.data.models import DataSourceType
from kontext_copilot.data.schemas._common import CamelAliasBaseModel


# Define the Pydantic schema for DataSource
class DataSourceModel(CamelAliasBaseModel):
    id: int
    name: str
    description: Optional[str] = None
    type: DataSourceType
    conn_str: str
    conn_str_encrypted: bool


# Create model excludes auto-generated fields like 'id'
class DataSourceCreateModel(CamelAliasBaseModel):
    name: str
    description: Optional[str] = None
    type: DataSourceType
    conn_str: str


# Update model makes all fields optional
class DataSourceUpdateModel(CamelAliasBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[DataSourceType] = None
    conn_str: Optional[str] = None


class SchemaTablesModel(CamelAliasBaseModel):
    schema_name: Optional[str]
    tables: list[str]


class ColumnInfoModel(CamelAliasBaseModel):
    name: str
    """column name"""

    primary_key: bool

    index: Optional[bool] = False

    unique: Optional[bool] = False

    data_type: str

    nullable: bool
    """boolean flag if the column is NULL or NOT NULL"""

    default: Optional[str]
    """column default expression as a SQL string"""

    autoincrement: Optional[bool] = None
    """database-dependent autoincrement flag.

    This flag indicates if the column has a database-side "autoincrement"
    flag of some kind.   Within SQLAlchemy, other kinds of columns may
    also act as an "autoincrement" column without necessarily having
    such a flag on them.

    See :paramref:`_schema.Column.autoincrement` for more background on
    "autoincrement".

    """

    comment: Optional[str] = None
    """comment for the column, if present.
    Only some dialects return this key
    """


class DataProviderInfoModel(DataSourceModel):
    supports_schema: bool
    metadata: List[SchemaTablesModel]


class SqlStatementModel(CamelAliasBaseModel):
    sql: str


class RunSqlResultModel(CamelAliasBaseModel):
    success: bool
    message: Optional[str]
    data: Any


class RunSqlPostBodyModel(CamelAliasBaseModel):
    sql: str
    schema_name: Optional[str] = None
    record_count: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[str] = None
    order_type: Optional[str] = None
