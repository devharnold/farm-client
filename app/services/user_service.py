# user service business logic
import uuid
from uuid import uuid4
import logging
import asyncpg
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.db import get_db_pool
from app.utils.token import create_access_token
from app.auth.password_utils import validate_password_strength, hash_password, verify_password

logging.basicConnfig(level=logging.INFO)

class UserService:
    def __init__(self, db_pool: asyncpg.pool.Pool):
        self.db_pool = db_pool

    async def register_user(self, email: str, password: str, phone: str, username: str, role: str):
        # Generate user_id and hash password
        user_id = str(uuid.uuid4())[:8]
        hashed_password = hash_password(password)

        # Check password strength
        if not validate_password_strength(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too weak!"
            )
        
        existing = await self.conn.fetchrow(
            "SELECT id FROM users WHERE email = $1 OR username = $2", email, username
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        
        try:
            row = await self.conn.fetchrow(
                "INSERT INTO users (id, username, email, password, role) VALUES ($1, $2, $3, $4, $5) RETURNING id",
                user_id, username, email, hashed_password, phone, role
            )
            return {"message": "User registered Successfully", "user_id": row["id"]}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error registering user: {str(e)}"
            )

    def get_user_by_email(self, email: str) -> None:
        try:
            self.cursor.execute("SELECT * FROM users WHERE email = %s", (email))
            user = self.cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            email = user
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Search failed!: str{e}"
            )

    def user_login(self, email: str, password: str):
        try:
            self.cursor.execute(
                "SELECT id, password FROM users WHERE email = %s", (email,)
            )
            user = self.cursor.fetchone()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user_id, hashed_password = user

            if not verify_password(password, hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password"
                )
            token = create_access_token({"user_id": user_id})
            return {"access_token": token}
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(e)}"
            )
