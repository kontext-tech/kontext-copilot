from datetime import datetime
from typing import Iterator

from kontext_copilot.copilot._session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool
from kontext_copilot.data.schemas import (
    ChatRoles,
    LlmChatMessage,
    RunSqlRequestModel,
    SessionMessageModel,
)


class RunSqlTool(BaseTool):
    def __init__(self, session: CopilotSession) -> None:
        super().__init__("Run SQL", session)

    def execute(self, request: RunSqlRequestModel, **kwargs):
        """
        Execute the tool
        """
        sql = request.sql
        max_records = request.max_records
        self.message = self.add_message(
            content="",
            role=ChatRoles.SYSTEM,
            is_streaming=True,
            copilot_generated=True,
        )
        response = self._run_sql(sql, max_records)
        return self._generate_response(response)

    def _run_sql(self, sql: str, max_records: int = 10) -> Iterator[str]:
        """
        Run SQL
        """
        self._logger.debug("Running SQL: %s", sql)
        # Create a new message

        yield "***SQL:***\n"
        yield f"```sql\n{sql}\n```\n"

        yield "\n***Results:***\n\n"
        try:
            result = self.data_provider.run_sql(sql)
            total_records = len(result)

            if total_records == 0:
                yield "0 records returned.\n"
            else:
                keys = result[0].keys()
                if total_records > max_records:
                    result = result[:max_records]
                    yield f"(showing first **{max_records}** records out of **{total_records}**).\n"

                yield "|"
                for col in keys:
                    yield f"{col}|"
                yield "\n"
                yield "|"
                for _ in keys:
                    yield "---|"
                yield "\n"
                for row in result:
                    yield "|"
                    for col in row.values():
                        yield f"{col}|"
                    yield "\n"
        except Exception as e:
            self._logger.error(f"Error running SQL: {e}")
            yield "\n**Error running SQL:**\n"
            yield f"```\n{e}\n```\n"

    def _generate_response(self, response: Iterator[str]):
        for res in response:
            message = SessionMessageModel(
                id=self.message.id,
                role=ChatRoles.SYSTEM,
                content=res,
                model="copilot",
                created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                done=False,
                copilot_generated=True,
                generating=True,
                session_id=self.session.session_id,
            )
            self.message.content += res
            yield message.model_dump_json(by_alias=True) + "\n"
            self.message.content += "\n"

        # Return a message to indicate the SQL execution is done
        yield SessionMessageModel(
            id=self.message.id,
            role=ChatRoles.SYSTEM,
            content="",
            model="copilot",
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            copilot_generated=True,
            done=True,
            generating=False,
            session_id=self.session.session_id,
        ).model_dump_json(by_alias=True) + "\n"
        self.commit_message(self.message)
        self.append_new_line(self.message.id, done=True)
