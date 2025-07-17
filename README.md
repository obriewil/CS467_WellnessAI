# WellnessAI (CS467 Online Capstone)
WellnessAI is a web-based application that empowers users to take control of their health through personalized, goal-driven guidance across fitness, nutrition, and stress management. By combining intelligent habit tracking with natural language support from a large language model (LLM), the app acts as a virtual wellness coach—offering daily encouragement, progress insights, and adaptive planning based on the user's evolving goals.

Unlike traditional health apps that isolate one aspect of wellness, WellnessAI blends goal prioritization, AI recommendations, and an intuitive user interface to promote long-term engagement and real, sustainable change.


# Project Overview
WellnessAI is a full-stack wellness web application designed to help users set and achieve personalized goals across nutrition, fitness, and stress management domains. The app uses an LLM (via OpenAI's API) to deliver daily affirmations, intelligent planning, goal recommendations, and conversational support based on user progress and preferences.

Key Features Include:
- Ranked goal-setting interface
- Daily check-ins and progress tracking
- Weekly AI-generated insights
- Integrated chat interface for support and planning
- Secure user authentication
- Scalable architecture with modular services

# Project Structure
CS467_WellnessAI/

|__ frontend/            # React-based UI

|__ backend/             # FastAPI backend

|__ benny-ai-service/    # Microservice that handles OpenAI LLM interactions

|__ bennyDB/    # Database for storing user information and daily check ins

|__ testing/    # Testing for individual features

|__ tests.py & tests.js/    # Regression testing files for checking before merges


# Prerequisites
Make sure you have the following installed:

- Node.js
- Python 3.9+
- PostgreSQL
- pip
- Git

# Running the App
## 1. Clone the repository

git clone https://github.com/obriewil/CS467_WellnessAI.git

cd CS467_WellnessAI


## 2. Run the Frontend

cd frontend

npm install

npm start

PORT: http://localhost:3000


## 3. Run the Backend (FastAPI)

### Installation
1. Create virtual env: `python -m venv backend`
2. Activate: `source backend/bin/activate` (Unix) or `backend\Scripts\activate` (Windows)
3. Install: `pip install -r requirements.txt`

### Configuration
Create `.env` file with:
- `SECRET_KEY=your_secure_random_string`
- Google: `GOOGLE_CLIENT_ID=your_id`, `GOOGLE_CLIENT_SECRET=your_secret`
- Apple: `APPLE_CLIENT_ID=your_id`, `APPLE_CLIENT_SECRET=your_secret`
- Facebook: `FACEBOOK_CLIENT_ID=your_id`, `FACEBOOK_CLIENT_SECRET=your_secret`

For local hosting, set redirect URIs in provider consoles to `http://127.0.0.1:8000/api/v1/auth/{provider}/callback`.

### Running
`uvicorn main:app --reload`

### Register apps on developer consoles:

- Google: console.cloud.google.com/apis/credentials → Create OAuth client ID (web app), get CLIENT_ID/SECRET, set redirect URI to http://127.0.0.1:8000/api/v1/auth/google/callback.

- Apple: developer.apple.com/account/resources/identifiers → Create Services ID, enable Sign in with Apple, get TEAM_ID/SERVICES_ID/PRIVATE_KEY, set redirect URI.

- Facebook: developers.facebook.com/apps → Create app, add Facebook Login product, get APP_ID/SECRET, set valid OAuth redirect URI.

Add credentials to .env (e.g., GOOGLE_CLIENT_ID=..., etc.).


## 4. Run the AI Service (Benny-AI-Service)

### Create Virtual Environment (MacOS/Linux)
cd benny-ai-service    

python -m venv benny-env 

source benny-env/bin/activate

pip install -r requirements.txt 


### Create Virtual Environment (Windows)
cd benny-ai-service 

python -m venv benny-env 

benny-env\Scripts\activate 

pip install -r requirements.txt 

*This microservice interfaces with the OpenAI API and handles prompt generation and AI logic.

### Run AI Service
cd src/api 

python main.py

PORT: http://localhost:8001

*Ensure this service is running before backend operations that require LLM calls.


# Running Tests
** NEED TO FILL IN**

# Tech Stack

Frontend: React, Tailwind CSS, React Router

Backend: FastAPI, PostgreSQL, SQLAlchemy

AI Service: Python + OpenAI API

Testing: **FILL IN** (frontend), Pytest (backend)

# Team Members

BriAnna Foreman – LLM integration, AI prompt engineering

James Liu – Frontend UI/UX & component development

Michael Jagielski – Backend databases and data flow

William O’Brien – DevOps, Full Stack, Integration

# License
MIT License

# Contact
For inquiries or contributions, feel free to open an issue or contact any team member.

