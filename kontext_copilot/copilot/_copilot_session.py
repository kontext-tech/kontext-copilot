from datetime import datetime
from typing import Optional

from kontext_copilot.copilot._prompt_factory import PromptFactory as pf
from kontext_copilot.data.schemas import (
    ChatRoles,
    CreateSessionMessageModel,
    CreateSessionModel,
    PromptNode,
    SessionMessageModel,
)
from kontext_copilot.services import (
    DataProviderService,
    get_data_sources_service,
    get_engine,
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
        data_source_id: Optional[int] = None,
        tables: Optional[list[str]] = None,
        schema_name: Optional[str] = None,
        session_id: Optional[int] = None,
    ):
        self.model = model
        self.data_source_id = data_source_id
        self.table_names = tables
        self.schema_name = schema_name
        self.session_id = session_id
        self._initialise()

    def _initialise(self):
        """
        Initialise the session
        """
        self._logger = get_logger()
        self._engine = get_engine()
        self._ds_service = get_data_sources_service(self._engine)
        self.session_service = get_session_service(self._engine)

        if self.data_source_id is not None:
            self.data_source = self._ds_service.get_data_source(self.data_source_id)
            self.data_provider = DataProviderService.get_data_provider(self.data_source)
        else:
            self.data_source = None
            self.data_provider = None

        self.tables = []

        if not self.table_names and self.data_source_id:
            self.tables = self.data_provider.get_all_tables_info(self.schema_name)
        elif self.table_names:
            for table in self.table_names:
                table_info = self.data_provider.get_table_info(table, self.schema_name)
                self.tables.append(table_info)

        self.system_prompt: PromptNode = None
        self._generate_system_prompt()

        # Add session object to the database
        self._create_or_update_session()

        self.data = {}

    def _get_shared_data_key(self, key: str, message: SessionMessageModel) -> str:
        return f"shared_data_{key}_{message.id}"

    def add_shared_data(self, message: SessionMessageModel, key: str, data: list[dict]):
        """
        Add shared data to the session
        """
        self._logger.debug("Adding shared data: %s", key)
        k = self._get_shared_data_key(key, message)
        self.data[k] = data

    def get_shared_data(
        self, message: SessionMessageModel, key: str
    ) -> Optional[list[dict]]:
        """
        Get shared data from the session
        """
        k = self._get_shared_data_key(key, message)
        return self.data.get(k, None)

    def _create_or_update_session(self):
        """
        Create a new session if session_id is not provided or update the existing session
        """
        session_exists = False
        if self.session_id:
            self.session_model = self.session_service.get_session(
                self.session_id, raise_error=False
            )
            if self.session_model is not None:
                session_exists = True

        if session_exists:
            # For chat messages request, data_source_id is not provided
            if self.data_source_id is not None:
                self._logger.info("Updating existing session: %s", self.session_id)
                self.session_model.system_prompt = self.system_prompt.get_prompt_str()
                self.session_model.data_source_id = self.data_source_id
                self.session_model.tables = self.table_names
                self.session_model.schema_name = self.schema_name
                self.session_model = self.session_service.update_session(
                    self.session_id, self.session_model
                )
            else:
                self.data_source_id = self.session_model.data_source_id
                self.table_names = self.session_model.tables
                self.schema_name = self.session_model.schema_name
        else:
            self._logger.info("Creating new session")
            created_at = datetime.now()

            if self.data_source:
                title = f"{self.data_source.name}-{self.schema_name if self.schema_name else 'default'}-{int(created_at.timestamp())}"
            else:
                title = f"General chat - {int(created_at.timestamp())}"

            session_create = CreateSessionModel(
                model=self.model,
                data_source_id=self.data_source_id,
                tables=self.table_names,
                schema_name=self.schema_name,
                system_prompt=self.system_prompt.get_prompt_str(),
                created_at=created_at,
                title=title,
            )
            self.session_model = self.session_service.create_session(session_create)
            self._logger.info("Session created: %s", self.session_model.id)

    def get_params(self):
        """
        Get the session parameters
        """

        return {
            "database_name": self.data_source.name,
            "database_type": self.data_source.type.name,
            "schema": self.schema_name,
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
            if self.data_source_id:
                self.system_prompt = pf.create_system_prompt(
                    self.data_source, self.tables, **self.get_params()
                )
            else:
                self.system_prompt = pf.create_default_system_prompt()

    def get_system_prompt(self) -> PromptNode:
        """
        Get the system prompt for the current session
        """
        if not self.system_prompt:
            self._generate_system_prompt()

        return self.system_prompt

    def get_fix_error_prompt(self, error: Exception) -> PromptNode:
        """
        Get the fix error prompt
        """
        return "Fix the following error in the above code:\n {error}".format(
            error=error
        )

    def get_sql_to_python_prompt(self, sql: str) -> PromptNode:
        """
        Get the SQL to Python prompt
        """
        return "Convert the following SQL to Python code:\n```sql\n{}```".format(sql)

    def get_sql_to_pyspark_prompt(self, sql: str) -> PromptNode:
        """
        Get the SQL to PySpark prompt
        """
        return "Convert the following SQL to PySpark code:\n```sql\n{}```".format(sql)

    def add_user_message(self, content: str):
        """
        Add user message to the session
        """
        message = CreateSessionMessageModel(
            session_id=self.session_model.id,
            content=content,
            role=ChatRoles.USER,
            is_system_prompt=False,
            is_streaming=False,
            copilot_generated=False,
            generating=False,
        )
        return self.session_service.add_session_message(
            self.session_model.id, message=message
        )
