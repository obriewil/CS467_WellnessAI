# Benny Backend README

## Installation
1. Create virtual env: `python -m venv backend`
2. Activate: `source backend/bin/activate` (Unix) or `backend\Scripts\activate` (Windows)
3. Install: `pip install -r requirements.txt`

## Configuration
Create `.env` file with:
- `SECRET_KEY=your_secure_random_string`
- Google: `GOOGLE_CLIENT_ID=your_id`, `GOOGLE_CLIENT_SECRET=your_secret`
- Apple: `APPLE_CLIENT_ID=your_id`, `APPLE_CLIENT_SECRET=your_secret`
- Facebook: `FACEBOOK_CLIENT_ID=your_id`, `FACEBOOK_CLIENT_SECRET=your_secret`

For local hosting, set redirect URIs in provider consoles to `http://127.0.0.1:8000/api/v1/auth/{provider}/callback`.

## Running
`uvicorn main:app --reload`

## Register apps on developer consoles:

- Google: console.cloud.google.com/apis/credentials → Create OAuth client ID (web app), get CLIENT_ID/SECRET, set redirect URI to http://127.0.0.1:8000/api/v1/auth/google/callback.

- Apple: developer.apple.com/account/resources/identifiers → Create Services ID, enable Sign in with Apple, get TEAM_ID/SERVICES_ID/PRIVATE_KEY, set redirect URI.

- Facebook: developers.facebook.com/apps → Create app, add Facebook Login product, get APP_ID/SECRET, set valid OAuth redirect URI.

Add credentials to .env (e.g., GOOGLE_CLIENT_ID=..., etc.).