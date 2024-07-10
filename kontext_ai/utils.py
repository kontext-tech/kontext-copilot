import logging
import os

from dotenv import load_dotenv

load_dotenv()

ENV_NAME = os.getenv("KONTEXT_AI_ENV", "development")
IS_LOCAL = ENV_NAME == "local"
CLIENT_APP_DIR = os.getenv("KONTEXT_AI_CLIENTAPP_DIR", "./ui")
HOST = os.getenv("KONTEXT_AI_HOST", "localhost")
PORT = int(os.getenv("KONTEXT_AI_PORT", "8100"))
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/kontext_ai.db"))
DB_URL = os.getenv("KONTEXT_AI_DB_URL", f"sqlite:///{DB_PATH}")
DEFAULT_MODEL = os.getenv("KONTEXT_AI_LLM_DEFAULT_MODEL", "phi3:mini")
DEFAULT_ENDPOINT = f"http://{HOST}:{PORT}"
DEFAULT_ENDPOINT_OLLAMA = os.getenv(
    "KONTEXT_AI_OLLAMA_ENDPOINT", "http://localhost:11434"
)
DEFAULT_USERNAME = os.getenv("KONTEXT_AI_APP_NAME", "Kontext User")


def get_logger(env: str = ENV_NAME) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(f"kontextAI{env}")


logger = get_logger()

logger.info("Environment: %s", ENV_NAME)
