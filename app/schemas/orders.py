from pydantic import BaseModel, EmailStr
from datetime import datetime

class PlaceOrderRequest(BaseModel):
    user_id: str
    product_id: str
    product_category: str
    farmer_id: str
    unit_price: float
    total_price: float
    created_at: datetime

class PlaceOrderResponse(BaseModel):
    user_id: str
    product_id: str
    order_id: str
    product_category: str
    total_price: float
    created_at: datetime
    updated_at: datetime

class ViewOrdersRequest(BaseModel):
    user_id: str

class ViewOrdersResponse(BaseModel):
    user_id: str
    product_id: str
    product_quantity: str
    total_price: float
    updated_at: datetime

class ViewCartRequest(BaseModel):
    product_id: str
    product_quantity: str
    unit_price: float
    total_price: float
    date_created: datetime

class ViewCartResponse(BaseModel):
    product_id: str
    product_quantity: str
    unit_price: float
    total_price: float
    date_created: datetime

class DeleteProductFromOrderRequest(BaseModel):
    product_id: str

class DeleteProductFromOrderResponse(BaseModel):
    product_id: str
    message: str