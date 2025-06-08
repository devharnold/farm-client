import psycopg2
import asyncpg
import os
from dotenv import load_dotenv
from fastapi import Request

load_dotenv()

db_pool = None

async def init_db_pool():
    db_pool = await asyncpg.create_pool(
        user=os.getenv(""),
        password=os.getenv(""),
        database=os.getenv(""),
        host=os.getenv(""),
        port=os.getenv(""),
        min_size=2,   # minimum number of connections
        max_size=10,  # maximum number of connections
    )

async def create_pool():
    return await asyncpg.create_pool(dsn="postgresql://user:password@localhost:5432/")

def get_db_pool(request: Request):
    return request.app.state.db_pool

