from typing import Optional

from kontext_copilot.copilot._prompt_factory import PromptFactory as pf
from kontext_copilot.copilot._types import PromptNode
from kontext_copilot.services import (
    DataProviderService,
    get_data_sources_service,
    get_db_engine,
)
from kontext_copilot.utils import get_logger


class Session:
    """
    A session object that holds the current context
    """

    def __init__(
        self, data_source_id: int, tables: Optional[list[str]], schema: Optional[str]
    ):
        self.data_source_id = data_source_id
        self.table_names = tables
        self.schema = schema
        self._initialise()

    def _initialise(self):
        """
        Initialise the session
        """
        self._logger = get_logger()
        self._engine = get_db_engine()
        self._ds_service = get_data_sources_service(self._engine)
        self.data_source = self._ds_service.get_data_source(self.data_source_id)
        if self.data_source is None:
            raise ValueError(f"Data source not found: {self.data_source_id}")
        self._data_provider = DataProviderService.get_data_provider(self.data_source)

        self.tables = []

        if not self.table_names:
            self.tables = self._data_provider.get_all_tables_info(self.schema)
        else:
            for table in self.table_names:
                table_info = self._data_provider.get_table_info(table, self.schema)
                self.tables.append(table_info)

        self.system_prompt: PromptNode = None

    def get_params(self):
        """
        Get the session parameters
        """
        return {
            "database_name": self.data_source.name,
            "database_type": self.data_source.type.name,
            "schema": self.schema,
        }

    def get_tables(self):
        """
        Get a list of tables
        """
        return self.tables

    def generate_system_prompt(self, force=False):
        """
        Generate a system prompt for the current session
        """
        if not self.system_prompt or force:
            self.system_prompt = pf.create_system_prompt(
                self.data_source, self.tables, **self.get_params()
            )

    def get_system_prompt(self) -> PromptNode:
        """
        Get the system prompt for the current session
        """
        if not self.system_prompt:
            self.generate_system_prompt()

        return self.system_prompt
