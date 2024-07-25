"""FastAPI app with Nuxt.js frontend"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from kontext_ai.api import llm, settings, prompts, data_sources, data_providers
from kontext_ai.utils import HOST, IS_LOCAL, CLIENT_APP_DIR, PORT

app = FastAPI()

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
    return {"message": f"Hello from {os.getenv('KONTEXT_AI_APP_NAME')}!"}


# Include the router in the FastAPI app
app.include_router(llm.llm_router)
app.include_router(settings.settings_router)
app.include_router(prompts.prompts_router)
app.include_router(data_sources.data_sources_router)
app.include_router(data_providers.data_providers_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
