from typing import List, Optional

from kontext_copilot.data.schemas._common import CamelAliasBaseModel


class LlmModelDetail(CamelAliasBaseModel):
    parent_model: str
    format: str
    family: str
    families: Optional[List[str]] = None
    parameter_size: str
    quantization_level: str


class LlmModel(CamelAliasBaseModel):
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: LlmModelDetail


class LlmModelListResponse(CamelAliasBaseModel):
    models: List[LlmModel]


class LlmChatMessage(CamelAliasBaseModel):
    role: str
    content: str


class LlmChatResponse(CamelAliasBaseModel):
    id: Optional[int] = None
    model: str
    created_at: str
    message: LlmChatMessage
    done: bool
    generating: Optional[bool] = False
    session_id: Optional[int] = None
    copilot_generated: bool = False
    is_system_prompt: Optional[bool] = False
