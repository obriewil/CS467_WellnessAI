"""API Server for Benny Wellness AI Endpoints"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio


# source path to import Benny
sys.path.append(str(Path(__file__).parent.parent))
from core.benny import BennyWellnessAI

# initialize benny
benny = None

# Start Benny
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Benny when API starts"""
    global benny
    benny = BennyWellnessAI()
    print("Benny API ready!")
    yield

app = FastAPI(title="Benny Wellness AI", lifespan=lifespan)

# Add CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

# REQUEST / RESPONSE MODEL
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    success: bool
    response: str
    tokens_used: int

# API ENDPOINTS
@app.get("/")
async def root():
    """Basic info endpoint"""
    return {"message": "Benny Wellness AI", "docs": "/docs"}


@app.get("/health")
async def health():
    """Benny health check"""
    return {"status": "healthy", "benny_ready": benny is not None}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
        Chat with Benny
        Timeout error handling/response
        Technical error handling/response
    """
    # Benny not responding
    if not benny:
        return ChatResponse(
            success=False,
            response="Benny is taking a break. Try again in a moment.",
            tokens_used=0
        )

    try:
        # timeout if no response from Benny
        result = await asyncio.wait_for(benny.chat(request.message), timeout=30.0)

        return ChatResponse(
            success=result["success"],
            response=result.get("response", "Sorry, something went wrong"),
            tokens_used=result.get("tokens_used", 0)
        )
    except asyncio.TimeoutError:
        return ChatResponse(
            success=False,
            response="Benny: I'm thinking extra hard, could you ask me again?",
            tokens_used=0
        )
    except Exception as e:
        print(f"Chat error: {e}")
        return ChatResponse(
            success=False,
            response="Benny: Having technical difficulties. Let's try again.",
            tokens_used=0
        )

# RUN SERVER

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
