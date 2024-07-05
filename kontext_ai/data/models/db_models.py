from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Settings(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)
