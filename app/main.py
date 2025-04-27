# FAST API entry

from fastapi import FastAPI
from app.routes import users

app = FastAPI(title = "Farm-Client API (RAW SQL)")

app.include_router(users.router, prefix="/api", tags=["Users"])

