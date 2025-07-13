from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from routers import auth  # Assuming auth.py is in routers folder

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secure_secret_key")
app.include_router(auth.router)