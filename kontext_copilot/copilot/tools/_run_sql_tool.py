from datetime import datetime
from typing import Iterator

from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool
from kontext_copilot.copilot.tools._charts_recommend_tool import ChartsRecommendTool
from kontext_copilot.data.schemas import (
    ActionsDataKeys,
    ActionTypes,
    ChatRoles,
    RunSqlRequestModel,
    SessionMessageModel,
)


class RunSqlTool(BaseTool):
    def __init__(self, session: CopilotSession) -> None:
        super().__init__("Run SQL", session)

    def execute(self, request: RunSqlRequestModel):
        """
        Execute the tool
        """
        self.sql = request.sql
        max_records = request.max_records
        self.message = self.add_message(
            content="",
            role=ChatRoles.SYSTEM,
            is_streaming=True,
            copilot_generated=True,
            parent_message_id=request.parent_message_id,
        )
        response = self._run_sql(self.sql, max_records)
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
                # Store result
                self.session.add_shared_data(
                    self.message, self.RUN_SQL_RESULT_DATA_KEY, result
                )

                # Generate response
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
            self.message.is_error = True
            self._logger.error(f"Error running SQL: {e}")
            yield "\n**Error running SQL:**\n"
            yield f"```\n{e}\n```\n"
            self.message.add_actions(
                [ActionTypes.FIX_SQL_ERRORS],
                {
                    ActionsDataKeys.FIX_SQL_ERRORS_PROMPT: self.session.get_fix_error_prompt(
                        e
                    )
                },
            )

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
                parent_message_id=self.message.parent_message_id,
            )
            self.message.content += res
            yield message.model_dump_json(by_alias=True) + "\n"
            self.message.content += "\n"

        # add actions to copy sql
        if not self.message.is_error:
            self.add_sql_related_actions(self.message, self.sql)
            self.add_recommend_charts_action(self.message)

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
            parent_message_id=self.message.parent_message_id,
            actions=self.message.actions,
        ).model_dump_json(by_alias=True) + "\n"
        self.commit_message(self.message)
        self.append_new_line(self.message.id, done=True)

    def add_recommend_charts_action(self, message: SessionMessageModel):
        """
        Add recommend charts action to the message
        """
        tool = ChartsRecommendTool(self.session)
        tool.execute(message)

    def add_sql_related_actions(self, message: SessionMessageModel, sql: str):
        """
        Add copy and other actions related to SQL to the message
        """
        message.init_actions()
        actions = [
            ActionTypes.COPY_SQL,
            ActionTypes.SQL_TO_PYTHON,
            # ActionTypes.SQL_TO_PYSPARK,
        ]
        self._logger.info("Adding actions: %s", actions)
        message.add_actions(
            actions,
            {
                ActionsDataKeys.SQL_TEXT: sql,
                ActionsDataKeys.SQL_TO_PYTHON_PROMPT: self.session.get_sql_to_python_prompt(
                    sql=sql
                ),
                # ActionsDataKeys.SQL_TO_PYSPARK_PROMPT: self.session.get_sql_to_pyspark_prompt(
                #     sql=sql
                # ),
            },
        )
