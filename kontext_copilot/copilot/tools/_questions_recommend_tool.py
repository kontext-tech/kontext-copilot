from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool


class QuestionsRecommendTool(BaseTool):
    def __init__(self, session: CopilotSession) -> None:
        super().__init__("Questions Recommend", session)

    def execute(self, **kwargs):
        pass
