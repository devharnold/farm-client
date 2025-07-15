import uuid
import logging
import asyncpg
from datetime import datetime
from fastapi import HTTPException, status
from app.db import get_db_pool
from app.auth.jwt_handler import create_access_token
from app.auth.password_utils import hash_password, validate_password_strength, verify_password

logging.basicConfig(level=logging.INFO)

class FarmerService:
    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def register_farmer(self, email: str, password: str, phone: str, username: str, role: str):
        # register a farmer into the platform
        farmer_id = str(uuid.uuid4())[:8]
        hashed_password = hash_password(password)

        if not validate_password_strength(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password strength is too weak"
            )
        
        existing = await self.conn.fetchrow(
            "SELECT id FROM farmers WHERE email = $1 OR username = $2", email, username
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User already exists"
            )
        
        try:
            row = await self.conn.fetchrow(
                "INSERT INTO farmers (id, username, email, password, phone, role) VALUES ($1, $2, $3, $4, $5, $6)",
                farmer_id, username, email, hashed_password, phone, role
            )
            return {"message": "Farmer registered successfully", "farmer_id": row["id"]}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error registering farmer."
            )
        
    def get_farmer_by_email(self, email: str) -> None:
        try:
            self.cursor.execute("SELECT * FROM farmers WHERE email = %s", (email))
            farmer = self.cursor.fetchone()

            if not farmer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            email = farmer

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Search failed!: str{e}"
            )


    async def farmer_login(self, email: str, password: str):
        async with self.db.acquire() as conn:
            farmer = await conn.fetchrow(
                "SELECT id, password FROM farmers WHERE email = $1", email
            )
            if not farmer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            if not verify_password(password, farmer["password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password"
                )

            token = create_access_token({"farmer_id": farmer["id"]})
            return {"access_token": token}
