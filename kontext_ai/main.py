"""FastAPI app with Nuxt.js frontend"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from kontext_ai.api import llm, settings, prompts
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

# Serve Nuxt app static files
if IS_LOCAL:
    app.mount("/ui", StaticFiles(directory=CLIENT_APP_DIR, html=True), name="ui")


@app.get("/api/hello")
async def hello():
    """Example FastAPI endpoint"""
    return {"message": f"Hello from {os.getenv('KONTEXT_AI_APP_NAME')}!"}


@app.get("/api/test_llm")
async def test_llm(prompt: str, max_length: int = 50):
    from kontext_ai.llms import LLMFactory

    llm = LLMFactory.get_llm()
    tokenizer = LLMFactory.get_tokenizer()

    # Encode the prompt to get input IDs
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate a response
    output_ids = llm.generate(input_ids, max_length=max_length, num_return_sequences=1)

    # Decode the output IDs to get the generated text
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return {"response": response}


# Include the router in the FastAPI app
app.include_router(llm.llm_router)
app.include_router(settings.settings_router)
app.include_router(prompts.prompts_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
