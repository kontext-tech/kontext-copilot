"""FastAPI app with Nuxt.js frontend"""

import os
from contextlib import asynccontextmanager

from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from kontext_copilot.api import copilot, data_providers, data_sources, prompts, settings
from kontext_copilot.data.schemas import ErrorResponseModel
from kontext_copilot.services import get_data_sources_service, get_engine
from kontext_copilot.utils import (
    CLIENT_APP_DIR,
    HOST,
    IS_DEV,
    IS_LOCAL,
    PORT,
    get_logger,
)

logger = get_logger()


def ensure_sample_data_source():
    dss = get_data_sources_service(get_engine())
    dss.ensure_sample_db()


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        logger.info("Starting Kontext Copilot")
        # Ensure sample database is added.
        ensure_sample_data_source()

        yield
    finally:
        logger.info("Shutting down Kontext Copilot")


app = FastAPI(lifespan=lifespan)

# CORS configuration
origins = [
    f"http://localhost:{PORT}",
    f"http://127.0.0.1::{PORT}",
]
if IS_DEV:
    origins.append("http://localhost:8101")
    origins.append("http://127.0.0.1:8101")

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


def run_migrations():
    # Get abs path of the ini file ./data/alembic/alembic.ini
    logger.critical("Running Alembic migrations")

    logger.info(f"Running migrations from script: {__file__}")

    config_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "data/alembic/alembic.ini"
    )

    current_working_directory = os.getcwd()

    # Define the working directory
    working_directory = os.path.abspath(os.path.dirname(config_path))
    # Change the current working directory
    os.chdir(working_directory)
    logger.info(f"Working directory: {working_directory}")

    logger.info(f"Using Alembic config file: {config_path}")

    alembic_cfg = Config(config_path)

    command.upgrade(alembic_cfg, "head")

    os.chdir(current_working_directory)
    logger.info(f"Changed working directory back to: {current_working_directory}")


def main():
    import uvicorn

    # Setup working directory
    wd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(wd)
    logger.info(f"Setup working directory: {wd}")

    # Run Alembric migrations
    run_migrations()

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )

    # Urls for the frontend
    logger.info(f"Frontend URL: http://{HOST}:{PORT}/ui")


if __name__ == "__main__":
    main()
