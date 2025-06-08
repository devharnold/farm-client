from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RegisterRequest(BaseModel): 
    email: EmailStr
    password: str
    username: str
    role: str

class GetUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    username: str
    user_id: str

class RegisterResponse(BaseModel):
    message: str
    farmer_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str

