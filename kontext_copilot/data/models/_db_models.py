from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SQLEnum,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)


class DataSourceType(str, Enum):
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


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_source_id = Column(Integer)
    tables = Column(String)
    schema = Column(String)
    title = Column(String)
    system_prompt = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    ended_at = Column(DateTime)


class SessionMessage(Base):
    __tablename__ = "session_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(
        Integer,
        ForeignKey("sessions.id"),
        index=True,
    )
    content = Column(String)
    role = Column(String)
    model = Column(String)
    done = Column(Boolean, default=False)
    copilot_generated = Column(Boolean, default=False)
    is_system_prompt = Column(Boolean, default=False)
    is_error = Column(Boolean, default=False)
    is_streaming = Column(Boolean, default=False)
    generating = Column(Boolean, default=False)
    actions = Column(String)
    created_at = Column(DateTime, default=datetime.now())
