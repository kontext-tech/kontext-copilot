from abc import abstractmethod

from kontext_copilot.copilot._session import CopilotSession
from kontext_copilot.services import DataProviderService
from kontext_copilot.utils import get_logger


class BaseTool:
    def __init__(self, tool_name: str, session: CopilotSession) -> None:
        self.tool_name = tool_name
        self._session = session
        self._logger = get_logger()
        self._initialise()

    def _initialise(self):
        """
        Initialise the tool
        """
        self.data_source = self._session.data_source
        self.data_provider = DataProviderService.get_data_provider(self.data_source)

    @abstractmethod
    def execute(self, **kwargs):
        pass
