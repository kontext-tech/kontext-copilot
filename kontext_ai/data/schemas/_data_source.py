from pydantic import BaseModel
from typing import Optional

from kontext_ai.data.models import DataSourceType, DataSource


# Define the Pydantic schema for DataSource
class DataSourceModel(BaseModel):
    id: Optional[int] = None
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
        orm_mode = True


# Create model excludes auto-generated fields like 'id'
class DataSourceCreateModel(BaseModel):
    name: str
    description: Optional[str] = None
    type: DataSourceType
    conn_str: str
    conn_str_encrypted: bool


# Update model makes all fields optional
class DataSourceUpdateModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[DataSourceType] = None
    conn_str: Optional[str] = None
    conn_str_encrypted: Optional[bool] = None
