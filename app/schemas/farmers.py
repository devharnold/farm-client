from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: str
    role: str

class RegisterResponse(BaseModel):
    message: str
    farmer_id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str

class AddProductRequest(BaseModel):
    farmer_id: str
    name: str
    category: str
    quantity: str
    price: float

class ProductResponse(BaseModel):
    product_id: str
    name: str
    category: str
    quantity: int
    price: float
    created_at: datetime
    updated_at: datetime


class DeleteProductResponse(BaseModel):
    message: str

class ResetQuantityResponse(BaseModel):
    message: str