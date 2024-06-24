from functools import wraps
from typing import Callable
from fastapi import HTTPException, Request
import ollama
from kontext_ai.api.llm._types import ModelsResponse


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
                detail=f"An unexpected error occurred when calling LLMs: [{e.status_code}] {e.error}") from e
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

    @error_handler
    def list(self, request: Request) -> ModelsResponse:
        json = self._client.list()
        return json
