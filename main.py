"""
Main entrypoint for the LLMInventory FastAPI application.

To run this application:
1. Install dependencies: pip install -r requirements.txt
2. Create and populate your secrets.yaml file.
3. Run the server: uvicorn main:app --reload
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import the main inventory class
from src.llminventory import LLMInventory

# --- Application Setup ---

# Define paths relative to the project root
PROJECT_ROOT = Path(__file__).parent
CONFIGS_DIR = PROJECT_ROOT / "configs"
SECRETS_FILE = PROJECT_ROOT / "secrets.yaml"

app = FastAPI(
    title="LLMInventory API",
    description="A unified API to interact with various Large Language Models.",
    version="0.1.0",
)

# Add CORS middleware to allow the web UI to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Inventory Instance (loaded at startup) ---

try:
    inventory = LLMInventory(configs_dir=CONFIGS_DIR, secrets_file=SECRETS_FILE)
except (NotADirectoryError, FileNotFoundError) as e:
    print(f"Fatal: Could not initialize LLMInventory. {e}")
    # In a real app, you might want to exit or prevent startup
    inventory = None
except Exception as e:
    print(f"An unexpected error occurred during initialization: {e}")
    inventory = None


# --- Pydantic Models for Request/Response ---

class ChatRequest(BaseModel):
    provider: str = Field(..., description="The name of the provider, e.g., 'openai' or 'anthropic'.")
    model: str = Field(..., description="The specific model name, e.g., 'gpt-4-turbo'.")
    payload: Dict[str, Any] = Field(..., description="The main request payload, containing required fields like 'messages'.")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Optional model parameters to override defaults, e.g., {'temperature': 0.7}.")

class ModelInfo(BaseModel):
    provider: str
    model: str
    description: str
    parameters: Dict[str, Any]
    required_fields: List[str]

class ModelsResponse(BaseModel):
    models: List[ModelInfo]

# --- API Endpoints ---

@app.get("/v1/models", response_model=ModelsResponse, tags=["Models"])
async def get_supported_models():
    """Returns a list of all supported models and their configurations."""
    if not inventory:
        raise HTTPException(status_code=503, detail="Inventory not available due to initialization error.")
    
    model_configs = inventory.get_supported_models()
    model_details = [ModelInfo(**config) for config in model_configs]
    return {"models": model_details}

@app.post("/v1/chat", tags=["Chat"])
async def chat_with_model(request: ChatRequest):
    """Sends a chat request to a specified model and returns the provider's response."""
    if not inventory:
        raise HTTPException(status_code=503, detail="Inventory not available due to initialization error.")

    try:
        response = inventory.invoke(
            provider=request.provider,
            model=request.model,
            payload=request.payload,
            parameters=request.parameters
        )
        return response
    except KeyError as e:
        # For missing model or missing API key
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        # For missing required fields or invalid params
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Service Unavailable: Could not connect to provider API. {e}")
    except Exception as e:
        # Catch-all for other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)