"""FastAPI app with Nuxt.js frontend"""

import os
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from kontext_ai.api.llm import LlmRequestsHandler

# Load environment variables without override
load_dotenv()

app = FastAPI()

is_local = os.getenv("KONTEXT_AI_ENV", "development") == "local"


client_app_dir = os.getenv("KONTEXT_AI_CLIENTAPP_DIR", "./client-app")

# Serve Nuxt app static files in development
if is_local:
    app.mount(
        "/client", StaticFiles(directory=client_app_dir, html=True), name="client-app"
    )


@app.get("/api/hello")
async def hello():
    """Example FastAPI endpoint"""
    return {"message": f"Hello from {os.getenv('KONTEXT_AI_APP_NAME')}!"}


# Define the router
router = APIRouter()

# Create an instance of the handler class
llm_handler = LlmRequestsHandler(
    endpoint=os.getenv("KONTEXT_AI_LLM_ENDPOINT", "http://localhost:11434"),
    default_model=os.getenv("KONTEXT_AI_LLM_DEFAULT_MODEL", "phi3:latest"),
)

# Add routes to the router
router.add_api_route("/list", llm_handler.list, methods=["GET"])

# Include the router in the FastAPI app
app.include_router(router, prefix="/api/llms")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("KONTEXT_AI_HOST", "localhost"),
        port=int(os.getenv("KONTEXT_AI_PORT", "8100")),
    )
