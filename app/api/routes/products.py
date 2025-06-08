from fastapi import APIRouter, HTTPException, Depends
from app.db import get_db_pool
from app.schemas.