from typing import List, Optional

import sys

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


class LlmModelDetail(TypedDict):
    parent_model: str
    format: str
    family: str
    families: Optional[List[str]]
    parameter_size: str
    quantization_level: str


class LlmModel(TypedDict):
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: LlmModelDetail


class ModelsResponse(TypedDict):
    models: List[LlmModel]
