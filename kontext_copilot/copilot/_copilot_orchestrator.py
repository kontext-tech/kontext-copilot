from typing import Optional

from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.copilot._prompt_factory import PromptFactory as pf
from kontext_copilot.copilot.tools._chart_renderer import ChartRenderer
from kontext_copilot.copilot.tools._llm_chat_tool import LlmChatTool
from kontext_copilot.copilot.tools._run_sql_tool import RunSqlTool
from kontext_copilot.data.schemas import (
    ChartDataRequestModel,
    ChartDataResponseModel,
    ChatRequestModel,
    RunSqlRequestModel,
)
from kontext_copilot.services import (
    DataProviderService,
    get_data_sources_service,
    get_engine,
)
from kontext_copilot.utils import get_logger


class CopilotOrchestrator:
    def __init__(self):
        self._logger = get_logger()
        self._engine = get_engine()
        self._ds_service = get_data_sources_service(self._engine)

    def init_session(
        self,
        model: str,
        data_source_id: Optional[int] = None,
        tables: Optional[list[str]] = None,
        schema: Optional[str] = None,
        session_id: Optional[int] = None,
    ) -> CopilotSession:
        """
        Initialise session for the copilot
        """
        self._logger.info("Initialising session for data source: %s", data_source_id)
        self.session = CopilotSession(model, data_source_id, tables, schema, session_id)
        return self.session

    def _check_session(self):
        if not self.session:
            raise ValueError("Session not initialised")

    def _get_provider(self, data_source_id: int):
        """
        Get the data provider based on the data source id.
        """
        try:
            self._logger.info(
                f"Retrieving data provider for data source id: {data_source_id}"
            )
            source = self._ds_service.get_data_source(data_source_id)
            provider = DataProviderService.get_data_provider(source)
            return provider
        except Exception as e:
            self._logger.error(
                f"Error retrieving data provider (#{data_source_id}): {e}"
            )
            raise e

    def run_sql(self, request: RunSqlRequestModel):
        """
        Run SQL
        """
        self._check_session()
        tool = RunSqlTool(self.session)
        return tool.execute(request=request)

    def chat(self, llm_host: str, request: ChatRequestModel):
        """
        Chat
        """
        self._check_session()
        tool = LlmChatTool(self.session)
        return tool.execute(llm_host=llm_host, request=request)

    def get_system_prompt(self):
        """
        Get system prompt
        """
        self._check_session()

        prompt = self.session.get_system_prompt()

        self._logger.debug("System prompt: %s", prompt)

        return prompt.get_prompt_str()

    def get_session_model(self):
        """
        Get the session model
        """
        self._check_session()
        return self.session.session_model

    def get_chart_data(self, request: ChartDataRequestModel) -> ChartDataResponseModel:
        """
        Get chart data
        """
        self._check_session()
        renderer = ChartRenderer(request)
        return renderer.render()
