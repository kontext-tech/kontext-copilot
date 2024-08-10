from pydantic import BaseModel


def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class CamelAliasBaseModel(BaseModel):

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class ErrorResponseModel(CamelAliasBaseModel):
    error: str
