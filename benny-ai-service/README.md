1. Set Up & Run
# create virtual environment
cd ai-service
python -m venv benny-env
source benny-env/bin/activate  # macOS/Linux benny-env\Scripts\activate   # Windows
pip install -r requirements.txt
# run
cd src/api
python main.py

port: http://127.0.0.1:8001

2. API Endpoints

HEALTH CHECK
GET /health

CHAT
POST /chat
Content-Type: application/json

{
    "message": "How can I eat more fiber?"
}

Response:

json 
{
    "success": true,
    "response": "Fiber is an important part of healthy digestion...",
    "tokens_used": 45
}

Test Benny in the Browser
Use http://127.0.0.1:8001/docs to test endpoints in the browser

Frontend Integration
chat function: fetch('http://localhost:8001/chat')


Citations
Claude AI used for planning and implementing chatbot development
