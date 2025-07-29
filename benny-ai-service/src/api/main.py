"""API Server for Benny Wellness AI Endpoints"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio

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
    allow_origins=["http://localhost:3000",
                   "http://127.0.0.1:3000", # frontend
                   "http://127.0.0.1:8000", # backend
                   "http://localhost:8000",
                   "http://127.0.0.1:5173", # vite
                   "http://localhost:5173"
                   ],
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
    error: Optional[str] = None

class DailyCheckInData(BaseModel):
    nutrition: str
    sleep: str
    fitness: str
    stress : str

class RecommendationRequest(BaseModel):
    daily_checkin: DailyCheckInData

# API ENDPOINTS
@app.get("/")
async def root():
    """Basic info endpoint"""
    return {
        "service": "Benny Wellness AI",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "recommend": "/recommend",
            "health": "/heath",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health():
    """Benny health check"""
    return {"status": "healthy", "benny_ready": benny is not None}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
        Chat with Benny
    """
    # Benny not responding
    if not benny:
        return ChatResponse(
            success=False,
            response="Benny is taking a break. Try again in a moment.",
            tokens_used=0
        )

    try:
        # Call benny with timeout
        result = await asyncio.wait_for(
            benny.chat(request.message), timeout=30.0)

        return ChatResponse(
            success=result["success"],
            response=result.get("response", ""),
            tokens_used=result.get("tokens_used", 0),
            error=result.get("error")
        )
    except asyncio.TimeoutError:
        return ChatResponse(
            success=False,
            response="Benny: I'm thinking extra hard, could you ask me again?",
            error="timeout"
        )
    except Exception as e:
        print(f"Chat error: {e}")
        return ChatResponse(
            success=False,
            response="Benny: Having technical difficulties. Let's try again.",
            error=str(e)
        )
    
@app.post("/recommend", response_model=ChatResponse)
async def recommend(request: RecommendationRequest):
    """
    Get wellness rec based on daily check-in
    """
    if not benny:
        return ChatResponse(
            success=False,
            response="Benny is taking a break. Try again later",
            tokens_used=0
        )
    try:
        # call benny with timeout
        result = await asyncio.wait_for(
            benny.recommend(request.daily_checkin.dict(exclude_unset=True)), timeout=30.0)
        
        return ChatResponse(
            success=result["success"],
            response=result.get("response", ""),
            tokens_used=result.get("tokens_used", 0),
            error=result.get("error")
        )
    except asyncio.TimeoutError:
        return ChatResponse(
            success=False,
            response="Benny is thinking extra hard. Try again later",
            tokens_used=0,
            error="timeout"
        )
    except Exception as e:
        print(f"Recommendation error: {e}")
        return ChatResponse(
            success=False,
            response="Benny is having technical difficulties. Try again later",
            tokens_used=0,
            error=str(e)
        )

# RUN SERVER

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
