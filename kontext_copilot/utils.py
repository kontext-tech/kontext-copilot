import inspect
import logging
import logging.config
import os

import colorlog

APP_DIR = os.path.abspath(os.path.dirname(__file__))

ENV_NAME = os.getenv("KONTEXT_COPILOT_ENV", "local")
IS_LOCAL = ENV_NAME == "local"
IS_DEV = ENV_NAME == "development"
CLIENT_APP_DIR = os.path.abspath(
    os.getenv("KONTEXT_COPILOT_CLIENTAPP_DIR", os.path.join(APP_DIR, "./ui"))
)
HOST = os.getenv("KONTEXT_COPILOT_HOST", "localhost")
PORT = int(os.getenv("KONTEXT_COPILOT_PORT", "8000"))
DB_PATH = os.path.abspath(os.path.join(APP_DIR, "data/kontext_copilot.db"))
ANA_DB_PATH = os.path.abspath(os.path.join(APP_DIR, "data/kontext_copilot.duckdb"))
ANA_DB_TABLE_PREFIX = "table_"
ANA_DB_VIEW_PREFIX = "view_"
DB_URL = os.getenv("KONTEXT_COPILOT_DB_URL", f"sqlite:///{DB_PATH}")
DEFAULT_MODEL = os.getenv("KONTEXT_COPILOT_LLM_DEFAULT_MODEL", "phi3:mini")
DEFAULT_ENDPOINT = f"http://{HOST}:{PORT}/llms"
DEFAULT_ENDPOINT_OLLAMA = os.getenv(
    "KONTEXT_COPILOT_OLLAMA_ENDPOINT", "http://localhost:11434"
)
DEFAULT_USERNAME = os.getenv("KONTEXT_COPILOT_APP_NAME", "User")

# Get absolute path of the logging config file
LOGGING_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "logging_config.ini")
logging.config.fileConfig(LOGGING_CONFIG_FILE, disable_existing_loggers=False)


def get_logger(env: str = ENV_NAME) -> logging.Logger:
    # Get the caller's module name
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    caller_module_name = caller_module.__name__ if caller_module else "unknown"
    logger_name = f"{env}.{caller_module_name}"
    return logging.getLogger(logger_name)


logger = get_logger()

logger.info("Environment: %s", ENV_NAME)


def get_db_path(db_name: str) -> str:
    """
    Get the absolute path of the database file.
    """
    return os.path.abspath(os.path.join(APP_DIR, "data", db_name))
