import json
from typing import (
    Iterator,
)
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from kontext_ai import ollama
from kontext_ai.api.llm._types import ModelsResponse
from kontext_ai.utils import get_logger
from kontext_ai.services import SettingsService, get_settings_service


router = APIRouter(
    tags=["llm"],
    prefix="/llms/api",
    responses={404: {"description": "Not found"}},
)

logger = get_logger()


def _get_client(settings_service: SettingsService) -> ollama.Client:
    settings = settings_service.get_settings_obj()
    return ollama.Client(
        host=settings.llm_ollama_endpoint,
    )


@router.get("/tags")
def list_models(
    settings_service: SettingsService = Depends(get_settings_service),
) -> ModelsResponse:
    """
    Get a list of available models.
    """
    logger.info("Getting list of models")
    response = _get_client(settings_service=settings_service).list()
    return response


@router.post("/chat")
async def chat(
    request: Request, settings_service: SettingsService = Depends(get_settings_service)
):
    """
    Generate a chat response using the requested model.
    """

    # Passing request body JSON to parameters of function _chat
    # Request body follows ollama API's chat request format for now.
    params = await request.json()
    logger.debug("Chat API invoked: %s", params)

    chat_response = _get_client(settings_service=settings_service).chat(**params)

    # Always return as streaming
    if isinstance(chat_response, Iterator):

        def generate_response():
            for response in iter(chat_response):
                yield json.dumps(response) + "\n"

        return StreamingResponse(generate_response(), media_type="application/x-ndjson")
    elif chat_response is not None:
        return json.dumps(chat_response)
