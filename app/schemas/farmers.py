from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: str
    created_at: datetime

class RegisterResponse(BaseModel):
    message: str
    farmer_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str

class GetFarmerRequest(BaseModel):
    email: str
    username: str
    phone: str
    farmer_id: str
