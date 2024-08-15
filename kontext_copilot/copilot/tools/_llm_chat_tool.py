from typing import Iterator

from kontext_copilot import ollama
from kontext_copilot.copilot._session import CopilotSession
from kontext_copilot.copilot.tools._base_tool import BaseTool
from kontext_copilot.data.schemas import ChatRequestModel, SessionMessageModel
from kontext_copilot.ollama._types import Message


def _to_pydantic_model(response) -> SessionMessageModel:
    # Convert message attribute in response to content and role
    message = response["message"]
    res = SessionMessageModel(
        content=message["content"],
        role=message["role"],
        **{k: v for k, v in response.items() if k != "message"},
    )
    return res


class LlmChatTool(BaseTool):
    def __init__(self, session: CopilotSession) -> None:
        super().__init__("LLM Chat", session)

    def execute(
        self,
        llm_host: str,
        request: ChatRequestModel,
        **kwargs,
    ):
        client = ollama.Client(
            host=llm_host,
        )

        params = request.model_dump(exclude_unset=True, exclude={"messages"})
        if request.messages is not None:
            params["messages"] = [
                Message(role=m.role, content=m.content) for m in request.messages
            ]

        # Remove keys that are not part of the chat API
        params = {
            k: v for k, v in params.items() if k in client.chat.__code__.co_varnames
        }
        self._logger.debug("Chat params: %s", params)

        chat_response = client.chat(**params)

        # Always return as streaming
        if isinstance(chat_response, Iterator):

            def generate_response():
                for response in iter(chat_response):
                    res = _to_pydantic_model(response)
                    yield res.model_dump_json(by_alias=True) + "\n"

            return generate_response()

        if chat_response is not None:
            res = _to_pydantic_model(chat_response)
            return res.model_dump_json(by_alias=True)
