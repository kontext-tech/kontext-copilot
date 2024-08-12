from kontext_copilot.copilot._session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool


class ExtractSqlTool(BaseTool):
    def __init__(self, session: CopilotSession) -> None:
        super().__init__("Extract SQL", session)

    def execute(self, **kwargs):
        pass
