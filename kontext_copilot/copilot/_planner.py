from typing import Optional
from kontext_copilot.copilot._prompt_factory import PromptFactory as pf
from kontext_copilot.copilot._session import Session
from kontext_copilot.services import (
    get_data_sources_service,
    get_db_engine,
)
from kontext_copilot.utils import get_logger


class Planner:
    def __init__(self):
        self._logger = get_logger()
        self._engine = get_db_engine()
        self._ds_service = get_data_sources_service(self._engine)

    def init_session(
        self, data_source_id: int, tables: Optional[list[str]], schema: Optional[str]
    ) -> Session:
        """
        Initialise session for the copilot
        """
        self._logger.info("Initialising session for data source: %s", data_source_id)
        self.session = Session(data_source_id, tables, schema)
        self._logger.info("Session initialised")
        return self.session

    def get_system_prompt(self):
        """
        Get system prompt
        """
        if not self.session:
            raise ValueError("Session not initialised")

        prompt = self.session.get_system_prompt()

        self._logger.debug("System prompt: %s", prompt)

        return prompt.get_prompt_str()
