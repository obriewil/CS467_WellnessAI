from fastapi import FastAPI, HTTPException
# from routers import auth  # Assuming auth.py is in routers folder 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import datetime
import aiohttp
import sys
from pathlib import Path


# add bennyDB directory to Python path
bennydb_path = Path(__file__).parent.parent/"bennyDB"
sys.path.append(str(bennydb_path))

import db_connector_real
db = db_connector_real.wellness_ai_db()
print("Database connected successfully!")

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
    allow_methods=["GET", "POST"],
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

@app.get("/")
async def root():
    """API info endpoint"""
    return {
        "service": "Benny Daily Check-in Backend",
        "database_connected": db is not None,
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
    """Submit daily check-in responses"""
    
    if not db:
        raise HTTPException(status_code=500, detail="Database not connected")

    try:
        # Get today's date
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        
        # Process the responses into the format the database expects
        checkin_data = {}
        
        for response in submission.responses:
            checkin_data[response.category] = response.response
        
        print(f"Saving check-in for {today}: {checkin_data}")
        
        # Simple database insert
        db.run_query("""
            INSERT INTO daily_log_table 
            (log_date, nutrition, sleep_quality, stress_level, activity_complete, activity_name, user_program_row_id, activity_addresses_goal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, today, checkin_data.get("nutrition"), checkin_data.get("sleep"), 
                checkin_data.get("stress"), 1, "Daily Check-in", 1, 1)
        
        print("Saved to database")


        # Get recommendation from Benny 
        recommendation = await get_benny_recommendation(checkin_data)

        return {
            "success": True,
            "message": "Check-in saved!",
            "data": checkin_data,
            "recommendation": recommendation
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

async def get_benny_recommendation(checkin_data):
    """Helper function to get recommendation from Benny"""
    try:
        benny_info = {
            "daily_checkin": {
                "nutrition": checkin_data.get("nutrition", ""),
                "sleep": checkin_data.get("sleep", ""),
                "fitness": checkin_data.get("fitness", ""),
                "stress": checkin_data.get("stress", "")
            }
        }
        print("Requesting Benny recommendation")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://127.0.0.1:8001/recommend",
                json=benny_info,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("Got Benny recommendation")
                    return result.get("response", "Great job on your check-in today!")
                else:
                    print(f"Benny Error: {response.status}")
                    return "Great job completing your check-in! Keep up the good work."
    except Exception as e:
        print(f"Benny unavailable: {e}")
        return "Great job completing your check-in! Keep up the good work."

           

if __name__ == "__main__":
    print("Starting Benny Daily Check-in Backend (Testing Mode)...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)