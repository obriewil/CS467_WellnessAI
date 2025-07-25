from fastapi import FastAPI, HTTPException
# from routers import auth  # Assuming auth.py is in routers folder 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import datetime

# Database import
import sys
from pathlib import Path

db = None
# add bennyDB directory to Python path
# bennydb_path = Path(__file__).parent.parent / "bennyDB"
# sys.path.append(str(bennydb_path))

# import db_connector_real
# db = db_connector_real.wellness_ai_db()
# print("Database connected successfully!")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite
        "http://localhost:3000",  # Create React App
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# app.include_router(auth.router)

# Pydantic models for request/response
class CheckInResponse(BaseModel):
    category: str
    question: str
    response: str

class CheckInSubmission(BaseModel):
    responses: List[CheckInResponse]

class CheckInResult(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

@app.get("/")
async def root():
    """API info endpoint"""
    return {
        "service": "Benny Daily Check-in Backend",
        "version": "1.0.0",
        "status": "running",
        "database_connected": db is not None,
        "endpoints": {
            "questions": "/api/checkin/questions",
            "submit": "/api/checkin/submit",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "database_connected": db is not None,
    }

@app.post("/api/checkin/submit")
async def submit_checkin(submission: CheckInSubmission):
    """Submit daily check-in responses (testing mode - no database)"""
    
    try:
        # Get today's date
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        
        print("=== RECEIVED CHECK-IN SUBMISSION ===")
        print(f"Date: {today}")
        print(f"Number of responses: {len(submission.responses)}")
        
        # Process and log the responses
        checkin_data = {}
        for response in submission.responses:
            print(f"Category: {response.category}")
            print(f"Question: {response.question}")
            print(f"Response: {response.response}")
            print("---")
            
            checkin_data[response.category] = response.response
        
        print("=== PROCESSED DATA ===")
        print(f"Checkin data: {checkin_data}")
        print("=== END SUBMISSION ===")
        
        return {
            "success": True,
            "message": "Check-in received successfully! (Testing mode - not saved to database)",
            "data": {
                "date": today,
                "responses": checkin_data,
                "total_responses": len(submission.responses)
            }
        }
        
    except Exception as e:
        print(f"Error processing check-in: {e}")
        raise HTTPException(status_code=500, detail=f"Submit error: {str(e)}")

if __name__ == "__main__":
    print("Starting Benny Daily Check-in Backend (Testing Mode)...")
    print("Database connection: DISABLED")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)