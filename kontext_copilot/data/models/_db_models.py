from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)


class DataSourceType(str, Enum):
    SQLite = "SQLite"
    DuckDB = "DuckDB"
    # PostgreSQL = "PostgreSQL"
    # MySQL = "MySQL"
    SQLServer = "SQLServer"
    # Oracle = "Oracle"
    # MongoDB = "MongoDB"
    # Redis = "Redis"


class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    type = Column(SQLEnum(DataSourceType, length=255))
    conn_str = Column(String)
    conn_str_encrypted = Column(Boolean, default=False)


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_source_id = Column(Integer)
    model = Column(String)
    tables = Column(String)
    schema_name = Column(String)
    title = Column(String)
    system_prompt = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    ended_at = Column(DateTime)
    messages: Mapped[List["SessionMessage"]] = relationship(
        "SessionMessage", back_populates="session"
    )


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
    parent_message_id = Column(Integer)
    done = Column(Boolean, default=False)
    copilot_generated = Column(Boolean, default=False)
    is_system_prompt = Column(Boolean, default=False)
    is_error = Column(Boolean, default=False)
    is_streaming = Column(Boolean, default=False)
    generating = Column(Boolean, default=False)
    actions = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    session: Mapped["Session"] = relationship(back_populates="messages")
