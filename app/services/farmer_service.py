# farmer service business logic
from app.db.connection import get_db_connection
from app.auth.password_utils import hash_password, validate_password_strength, verify_password
from app.auth.jwt_handler import create_access_token
from fastapi import HTTPException, status
from datetime import datetime
import uuid
from uuid import uuid4

class FarmerService:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def register_farmer(self, email: str, password: str, username: str, role: str):
        # Generate farmer_id
        farmer_id = str(uuid.uuid4())
        hashed_password = hash_password(password)

        # Check password strength
        if not validate_password_strength(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password strength is too weak"
            )
        
        # Check if the farmer already exists in the database
        self.cursor.execute("SELECT id FROM farmers WHERE email = %s AND username = %s", (email, username))
        if self.cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Farmer with this email or username already exists"
            )
        
        try:
            # Insert the farmer into the database
            self.cursor.execute(
                "INSERT INTO farmers (id, )"
            )