from enum import Enum
from sqlalchemy import Boolean, Column, Integer, String, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)


class DataSourceType(Enum):
    SQLite = "SQLite"
    # DuckDB = "DuckDB"
    # PostgreSQL = "PostgreSQL"
    # MySQL = "MySQL"
    # SQLServer = "SQLServer"
    # Oracle = "Oracle"
    # MongoDB = "MongoDB"
    # Redis = "Redis"


class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    type = Column(SQLEnum(DataSourceType))
    conn_str = Column(String)
    conn_str_encrypted = Column(Boolean, default=False)
