from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware 
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import datetime
import sys
from pathlib import Path
from config import SECRET_KEY
from routers import auth, users

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
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(users.router)

# Add OUATH middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

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
        
        print(f"Saved to database")

        return {
            "success": True,
            "message": "Check-in saved!",
            "data": checkin_data
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/chat/recent")
async def get_recent_chat_messages():
    """Get the last 10 recent chat messages"""

    if not db:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    try:
        # get database chat history
        query = """
        SELECT
            che.sequence_number,
            che.user_or_benny,
            che.entry_text,
            ch.date
        FROM chat_history_entries che
        JOIN chat_history ch ON che.fk_row_id =  ch.row_id
        ORDER BY ch.date DESC, che.sequence_number DESC
        LIMIT 10
        """

        result = db.run_query(query)
        messages = result.fetchall()

        # format response
        formatted_messages = []
        for message in messages:
            formatted_messages.append({
                "sequence_number": message[0],
                "user_or_benny": message[1],
                "entry_text": message[2],
                "date": message[3]
            })

        formatted_messages.reverse()
        return {
            "success": True,
            "messages": formatted_messages
        }
    
    except Exception as e:
        print(f"Error fetching recent messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))
           

if __name__ == "__main__":
    print("Starting Benny Daily Check-in Backend (Testing Mode)...")
    print("Database connection: DISABLED")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)