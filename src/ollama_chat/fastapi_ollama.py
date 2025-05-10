from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .ollama_client import OllamaClient

# Custom OpenAPI schema metadata
app = FastAPI(
    title="Ollama Gemma Chat API",
    description="A REST API for interacting with the Ollama (Gemma) language model. Accepts chat messages and returns model responses.",
    version="1.0.0",
    contact={
        "name": "Guanacos Project",
        "url": "https://github.com/janogelin/guanacos",
        "email": "digicloseup@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc UI
)

# Request schema for chat endpoint
class ChatRequest(BaseModel):
    message: str  # The user's message to send to the model
    system_prompt: str = None  # Optional system prompt to set context

# Response schema for chat endpoint
class ChatResponse(BaseModel):
    response: str  # The model's response as a single string

# Initialize the Ollama client (default to gemma3:4b)
ollama_client = OllamaClient(model="gemma3:4b")

@app.post("/chat", response_model=ChatResponse, summary="Chat with the Gemma model", tags=["Chat"])
def chat_endpoint(request: ChatRequest):
    """
    Send a chat message to the Ollama (Gemma) model and receive a response.
    - **message**: The user's message to send to the model.
    - **system_prompt**: (Optional) System prompt to set the model's context.
    """
    if request.system_prompt:
        ollama_client.set_system_prompt(request.system_prompt)
    try:
        # Collect the streamed response into a single string
        response_chunks = []
        for chunk in ollama_client.chat(request.message):
            if chunk.startswith("Error:"):
                raise HTTPException(status_code=500, detail=chunk)
            response_chunks.append(chunk)
        return ChatResponse(response="".join(response_chunks))
    except Exception as e:
        # Return a 500 error if anything goes wrong
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz", summary="Health check", tags=["Health"])
def health_check():
    """
    Check if the Ollama server and model are available.
    Returns status and connection message.
    """
    success, message = ollama_client.check_connection()
    if not success:
        raise HTTPException(status_code=503, detail=message)
    return {"status": "ok", "message": message} 