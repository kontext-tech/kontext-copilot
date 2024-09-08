from typing import Optional, Union

from kontext_copilot.data.schemas._common import CamelAliasBaseModel
from kontext_copilot.utils import (
    DEFAULT_ENDPOINT,
    DEFAULT_ENDPOINT_OLLAMA,
    DEFAULT_MODEL,
    DEFAULT_USERNAME,
)


class SettingBaseModel(CamelAliasBaseModel):
    key: str
    value: Union[str, int, float, None] = None


class SettingCreateModel(SettingBaseModel):
    pass


class SettingUpdateModel(SettingBaseModel):
    pass


class SettingModel(SettingBaseModel):

    class Config:
        from_attributes = True


class GeneralSettingsModel(CamelAliasBaseModel):
    """
    Model for general settings.
    """

    general_theme: str = "light"
    general_username: str = DEFAULT_USERNAME


class LlmSettingsModel(CamelAliasBaseModel):
    """
    Model for LLM settings.
    """

    llm_default_model: str = DEFAULT_MODEL
    llm_temperature: float = 0.1
    # llm_max_tokens: int = 100
    llm_top_p: float = 0.95
    llm_top_k: float = 40
    # llm_frequency_penalty: float = 0.0
    # llm_presence_penalty: float = 0.0
    # llm_stop_sequence: str = None
    llm_api_key: Optional[str] = ""
    llm_endpoint: str = DEFAULT_ENDPOINT
    llm_ollama_endpoint: str = DEFAULT_ENDPOINT_OLLAMA
    llm_seed: int = 100


class SettingsModel(GeneralSettingsModel, LlmSettingsModel):
    pass
