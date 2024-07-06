from typing import Union

from pydantic import BaseModel


class SettingBase(BaseModel):
    key: str
    value: Union[str, None] = None


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    pass


class Setting(SettingBase):

    class Config:
        from_attributes = True


class GeneralSettings(BaseModel):
    """
    Model for general settings.
    """

    general_theme: str = "light"
    general_username: str = "Kontext User"


class LlmSettings(BaseModel):
    """
    Model for LLM settings.
    """

    llm_default_model: str = "phi3:latest"
    llm_temperature: float = 0.5
    # llm_max_tokens: int = 100
    # llm_top_p: float = 1.0
    # llm_frequency_penalty: float = 0.0
    # llm_presence_penalty: float = 0.0
    # llm_stop_sequence: str = None
    llm_api_key: str = None
    llm_endpoint: str = "http://localhost:8100/llms"
    llm_ollama_endpoint: str = "http://localhost:11434"


class Settings(GeneralSettings, LlmSettings):
    pass
