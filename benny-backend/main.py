from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import datetime
import sys
from pathlib import Path

# --- Imports for Auth ---
from config import SECRET_KEY
from routers import auth, users

# --- Database Setup ---
bennydb_path = Path(__file__).parent.parent / "bennyDB"
sys.path.append(str(bennydb_path))
import db_connector_real
db = db_connector_real.wellness_ai_db()
print("Database connected successfully!")

# --- App Initialization ---
app = FastAPI()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# --- Include Routers ---
app.include_router(auth.router)
app.include_router(users.router)

# --- Pydantic Models ---
class CheckInResponse(BaseModel):
    category: str
    question: str
    response: str

class CheckInSubmission(BaseModel):
    responses: List[CheckInResponse]

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"service": "Benny Daily Check-in Backend"}

@app.post("/api/checkin/submit")
async def submit_checkin(submission: CheckInSubmission):
    try:
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        checkin_data = {res.category: res.response for res in submission.responses}
        db.run_query("""
            INSERT INTO daily_log_table (log_date, nutrition, sleep_quality, stress_level)
            VALUES (?, ?, ?, ?)
        """, today, checkin_data.get("nutrition"), checkin_data.get("sleep"), checkin_data.get("stress"))
        return {"success": True, "message": "Check-in saved!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Run Block ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)