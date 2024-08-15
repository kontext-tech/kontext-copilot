"""FastAPI app with Nuxt.js frontend"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from kontext_copilot.api import copilot, data_providers, data_sources, prompts, settings
from kontext_copilot.data.schemas import ErrorResponseModel
from kontext_copilot.utils import CLIENT_APP_DIR, HOST, IS_LOCAL, PORT, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = get_logger()
    try:
        logger.info("Starting Kontext Copilot")
        yield
    finally:
        logger.info("Shutting down Kontext Copilot")


app = FastAPI(lifespan=lifespan)

# CORS configuration
origins = [
    "http://localhost:8101",
    "http://127.0.0.1:8101",
    f"http://localhost:{PORT}",
    f"http://127.0.0.1::{PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)

# Serve Nuxt app static files in development
if IS_LOCAL:
    app.mount("/ui", StaticFiles(directory=CLIENT_APP_DIR, html=True), name="ui")


@app.get("/api/hello")
async def hello():
    """Example FastAPI endpoint"""
    return {"message": f"Hello from {os.getenv('KONTEXT_COPILOT_APP_NAME')}!"}


# Include the router in the FastAPI app
app.include_router(settings.settings_router)
app.include_router(prompts.prompts_router)
app.include_router(data_sources.data_sources_router)
app.include_router(data_providers.data_providers_router)
app.include_router(copilot.copilot_router)


# Generic error handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponseModel(
            error="Internal Server Error", detail=str(exc)
        ).model_dump_json(),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
