from enum import Enum
from typing import Optional

from pydantic import BaseModel


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class CamelAliasBaseModel(BaseModel):

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True

    @classmethod
    def from_db_model(cls, db_model):
        """
        Converts a database model to a Pydantic model.
        """
        return cls.model_validate(db_model)


class ErrorResponseModel(CamelAliasBaseModel):
    error: str
    detail: Optional[str] = None


class ChatRoles(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
