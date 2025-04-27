# user service business logic
from app.db.connection import get_db_connection
from app.auth.password_utils import hash_password, verify_password, validate_password_strength
from app.auth.jwt_handler import create_access_token
from fastapi import HTTPException, status
import uuid
from uuid import uuid4

class UserService:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def register_user(self, email: str, password: str, username: str, role: str):
        # Generate user_id and hash password
        user_id = str(uuid.uuid4())[:8]
        hashed_password = hash_password(password)

        # Check password strength
        if not validate_password_strength(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is too weak, Ensure it contains the requirements!"
            )
        
        # Check if the user already exists
        self.cursor.execute("SELECT id FROM users WHERE email = %s OR username = %s", (email, username))
        if self.cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        try:
            # Insert new user into the database
            self.cursor.execute(
                "INSERT INTO users (id, username, email, password, role) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (user_id, username, email, hashed_password, role)
            )
            user_id = self.cursor.fetchone()[0]
            self.conn.commit()

            return {"message": "User registered successfully", "user_id": user_id}
        
        except Exception as e:
            self.conn.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while registering the user: {str(e)}"
            )
        finally:
            self._cleanup

    def _cleanup(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()