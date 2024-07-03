import asyncio
from functools import wraps
import json
import logging
from typing import (
    Annotated,
    Any,
    Callable,
    Iterator,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Union,
)
from fastapi import Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from kontext_ai import ollama
from kontext_ai.api.llm._types import ModelsResponse
from kontext_ai.utils import get_logger


def error_handler(func: Callable) -> Callable:
    """
    A decorator to handle errors uniformly for class methods.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ollama.ResponseError as e:
            # Log the error or perform any additional actions
            print(f"A server error occurred: {e.error}")
            # Raise an HTTPException with a specific status code and detail
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred when calling LLMs: [{e.status_code}] {e.error}",
            ) from e

    return wrapper


class LlmRequestsHandler:
    """
    This class handles the requests for LLM (Large Language Model).
    """

    _client: ollama.Client = None

    def __init__(self, endpoint: str, default_model: str, api_key: str = None):
        self.endpoint = endpoint
        self.default_model = default_model
        self.api_key = api_key
        self._client = ollama.Client(host=endpoint)
        self.logger = get_logger()

    def list(self) -> ModelsResponse:
        """
        Get a list of available models.
        """
        response = self._client.list()
        return response

    async def chat(self, request: Request):
        """
        Generate a chat response using the requested model.
        """

        # Passing request body JSON to parameters of function _chat
        # Request body follows ollama API's chat request format for now.
        params = await request.json()
        self.logger.debug("Request data: %s", params)

        chat_response = self._client.chat(**params)

        # Always return as streaming
        if isinstance(chat_response, Iterator):

            def generate_response():
                for response in chat_response:
                    yield json.dumps(response) + "\n"

            return StreamingResponse(
                generate_response(), media_type="application/x-ndjson"
            )
        elif chat_response is not None:
            return json.dumps(chat_response)
