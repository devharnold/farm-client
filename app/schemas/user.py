from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegisterRequest(BaseModel): 
    email: EmailStr
    password: str
    username: str
    phone: str
    role: str
    created_at: datetime

class GetUserRequest(BaseModel):
    email: EmailStr

class GetUserResponse(BaseModel):
    email: EmailStr
    username: str
    phone: str
    user_id: str

class RegisterResponse(BaseModel):
    message: str
    farmer_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str

