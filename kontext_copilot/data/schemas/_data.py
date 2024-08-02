import sys
from pydantic import BaseModel
from typing import Any, List, Optional
from kontext_copilot.data.models import DataSourceType, DataSource

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict, NotRequired
else:
    from typing import TypedDict, NotRequired


# Define the Pydantic schema for DataSource
class DataSourceModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    type: DataSourceType
    conn_str: str
    conn_str_encrypted: bool

    @classmethod
    def from_db_model(cls, source: DataSource) -> "DataSourceModel":
        """Build schema based of db model provided."""

        return cls(
            id=source.id,
            name=source.name,
            description=source.description,
            type=source.type,
            conn_str=source.conn_str,
            conn_str_encrypted=source.conn_str_encrypted,
        )

    class Config:
        from_attributes = True


# Create model excludes auto-generated fields like 'id'
class DataSourceCreateModel(BaseModel):
    name: str
    description: Optional[str] = None
    type: DataSourceType
    conn_str: str


# Update model makes all fields optional
class DataSourceUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[DataSourceType] = None
    conn_str: Optional[str] = None


class SchemaTablesModel(TypedDict):
    schema: Optional[str]
    tables: list[str]


class ColumnInfoModel(TypedDict):
    name: str
    """column name"""

    primary_key: bool

    index: Optional[bool]

    unique: Optional[bool]

    data_type: str

    nullable: bool
    """boolean flag if the column is NULL or NOT NULL"""

    default: Optional[str]
    """column default expression as a SQL string"""

    autoincrement: NotRequired[bool]
    """database-dependent autoincrement flag.

    This flag indicates if the column has a database-side "autoincrement"
    flag of some kind.   Within SQLAlchemy, other kinds of columns may
    also act as an "autoincrement" column without necessarily having
    such a flag on them.

    See :paramref:`_schema.Column.autoincrement` for more background on
    "autoincrement".

    """

    comment: NotRequired[Optional[str]]
    """comment for the column, if present.
    Only some dialects return this key
    """


class DataProviderInfoModel(DataSourceModel):
    supports_schema: bool
    metadata: List[SchemaTablesModel]


class SqlStatementModel(TypedDict):
    sql: str


class RunSqlResultModel(TypedDict):
    success: bool
    message: Optional[str]
    data: Any


class RunSqlPostBodyModel(TypedDict):
    sql: str
    schema: NotRequired[str]
    record_count: NotRequired[int]
    offset: NotRequired[int]
    order_by: NotRequired[str]
    order_type: NotRequired[str]
