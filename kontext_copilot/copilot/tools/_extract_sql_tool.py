import re

from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool
from kontext_copilot.data.schemas import (
    ActionsDataKeys,
    ActionTypes,
    CodeBlockModel,
    SessionMessageModel,
)


class ExtractSqlTool(BaseTool):
    """Extract SQL from markdown content"""

    def __init__(self, session: CopilotSession) -> None:
        super().__init__("Extract SQL", session)

    def execute(self, message: SessionMessageModel) -> None:
        """Extract sql"""
        self._logger.info("Extracting SQL from message: %s", message.content)
        code_blocks = self._extract_code(message.content)
        # Find all sql code blocks
        sql_code_blocks = [
            code_block for code_block in code_blocks if code_block.language == "sql"
        ]
        if len(sql_code_blocks) > 0:
            message.init_actions()
            self._logger.info("Adding actions: %s", ActionTypes.RUN_SQL)
            message.add_actions(
                [ActionTypes.RUN_SQL],
                {ActionsDataKeys.SQL_LIST: [cb.code for cb in sql_code_blocks]},
            )

    def _extract_code(self, markdown: str) -> list[CodeBlockModel]:
        """Extract code blocks from markdown content"""

        pattern = r"```\s*(?P<language>\w+)?(?P<code>.*?)```"

        # find all the matches of language and code blocks and convert to dictionary
        matches = re.finditer(pattern, markdown, re.DOTALL)

        return [
            CodeBlockModel(
                language=match.group("language") or "unknown", code=match.group("code")
            )
            for match in matches
        ]
