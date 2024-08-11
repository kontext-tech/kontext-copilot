from typing import Optional

from kontext_copilot.copilot._prompt_factory import PromptFactory as pf
from kontext_copilot.copilot._types import PromptNode
from kontext_copilot.data.schemas import CreateSessionModel
from kontext_copilot.services import (
    DataProviderService,
    get_data_sources_service,
    get_db_engine,
    get_session_service,
)
from kontext_copilot.utils import get_logger


class CopilotSession:
    """
    A session object that holds the current context
    """

    def __init__(
        self,
        model: str,
        data_source_id: int,
        tables: Optional[list[str]],
        schema: Optional[str],
    ):
        self.model = model
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
        self._session_service = get_session_service(self._engine)
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
        self._generate_system_prompt()

        # Add session object to the database
        self._create_session()

    def _create_session(self):
        """
        Create a new session
        """
        session_create = CreateSessionModel(
            model=self.model,
            data_source_id=self.data_source_id,
            tables=",".join(self.table_names),
            schema_name=self.schema,
            system_prompt=self.system_prompt.get_prompt_str(),
        )
        self.session_model = self._session_service.create_session(session_create)

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

    def _generate_system_prompt(self, force=False):
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
            self._generate_system_prompt()

        return self.system_prompt
