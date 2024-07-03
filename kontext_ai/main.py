"""FastAPI app with Nuxt.js frontend"""

import os
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from kontext_ai.api.llm import LlmRequestsHandler
from kontext_ai.utils import HOST, IS_LOCAL, CLIENT_APP_DIR, PORT

app = FastAPI()

# Serve Nuxt app static files in development
if IS_LOCAL:
    app.mount(
        "/client", StaticFiles(directory=CLIENT_APP_DIR, html=True), name="client-app"
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
router.add_api_route("/tags", llm_handler.list, methods=["GET"])
router.add_api_route("/chat", llm_handler.chat, methods=["POST"])

# Include the router in the FastAPI app
app.include_router(router, prefix="/llms/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
