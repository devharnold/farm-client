from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AddProductRequest(BaseModel):
    farmer_id: str
    product_name: str
    product_category: str
    product_quantity: str
    product_price: float
    product_id: str

class AddProductResponse(BaseModel):
    product_id: str
    product_name: str
    product_category: str
    product_quantity: int
    product_price: float
    created_at: datetime
    updated_at: datetime

class FindProductRequest(BaseModel):
    product_id: str

class FindProductResponse(BaseModel):
    product_id: str
    product_name: str
    product_category: str
    product_price: float

class UpdateQuantityRequest(BaseModel):
    product_id: str
    product_quantity: int

class UpdateQuantityResponse(BaseModel):
    product_id: str
    product_name: str
    product_quantity: int

class ResetQuantityRequest(BaseModel):
    product_id: str
    product_quantity: int

class ResetQuantityResponse(BaseModel):
    product_id: str
    product_quantity: int

class DeleteProductRequest(BaseModel):
    product_id: str

class DeleteProductResponse(BaseModel):
    product_id: str
    message: str
