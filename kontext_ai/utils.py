import logging
import os

from dotenv import load_dotenv

load_dotenv()

ENV_NAME = os.getenv("KONTEXT_AI_ENV", "development")
IS_LOCAL = ENV_NAME == "local"
CLIENT_APP_DIR = os.getenv("KONTEXT_AI_CLIENTAPP_DIR", "./client-app")
HOST = (os.getenv("KONTEXT_AI_HOST", "localhost"),)
PORT = int(os.getenv("KONTEXT_AI_PORT", "8100"))


def get_logger(env: str = ENV_NAME) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(f"kontext_ai_{env}")


logger = get_logger()

logger.info("Environment: %s", ENV_NAME)
