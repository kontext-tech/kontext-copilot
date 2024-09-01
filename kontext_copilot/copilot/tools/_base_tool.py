from abc import abstractmethod
from typing import Optional

from kontext_copilot.copilot._copilot_session import CopilotSession
from kontext_copilot.data.schemas import (
    ChatRoles,
    CreateSessionMessageModel,
    SessionMessageModel,
    UpdateSessionMessageModel,
)
from kontext_copilot.utils import get_logger


class BaseTool:

    RUN_SQL_RESULT_DATA_KEY = "run_sql_result"

    def __init__(self, tool_name: str, session: CopilotSession) -> None:
        self.tool_name = tool_name
        self.session = session
        self._logger = get_logger()
        self._initialise()

    def _initialise(self):
        """
        Initialise the tool
        """
        self.data_source = self.session.data_source
        self.data_provider = self.session.data_provider
        self.data = {}

    @abstractmethod
    def execute(self, **kwargs):
        pass

    def add_message(
        self,
        content: str,
        role: ChatRoles = ChatRoles.SYSTEM,
        is_system_prompt: bool = False,
        is_streaming: bool = False,
        copilot_generated: bool = True,
        generating: bool = True,
        parent_message_id: Optional[int] = None,
    ) -> SessionMessageModel:
        """
        Add a new message to the session
        """
        self._logger.debug(
            "Adding message: %s, role: %s, is_system_prompt: %s, is_streaming: %s, copilot_generated: %s, generating: %s",
            content,
            role,
            is_system_prompt,
            is_streaming,
            copilot_generated,
            generating,
            parent_message_id,
        )
        message_model = CreateSessionMessageModel(
            session_id=self.session.session_id,
            content=content,
            role=role,
            is_system_prompt=is_system_prompt,
            is_streaming=is_streaming,
            copilot_generated=copilot_generated,
            generating=generating,
            parent_message_id=parent_message_id,
        )
        return self.session.session_service.add_session_message(
            self.session.session_id, message_model
        )

    def append_message_part(
        self, message_id: int, message_part: str, done: bool = False
    ) -> SessionMessageModel:
        """
        Append a message part to the message and persite in storage
        """
        self._logger.debug(
            "Appending message part: %s to message: %s", message_part, message_id
        )
        return self.session.session_service.append_message_part(
            self.session.session_id, message_id, message_part, done
        )

    def commit_message(self, message: SessionMessageModel) -> SessionMessageModel:
        """
        Commit the message
        """
        self._logger.debug("Committing message: %s", message)
        return self.session.session_service.update_session_message(
            self.session.session_id,
            message_id=message.id,
            message_update=UpdateSessionMessageModel(
                content=message.content,
                generating=False,
                done=True,
                actions=message.actions,
            ),
        )

    def append_new_line(
        self, message_id: int, done: bool = False
    ) -> SessionMessageModel:
        """
        Append a new line to the message
        """
        return self.append_message_part(message_id, "\n", done)
