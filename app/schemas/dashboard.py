from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class FarmerDashboardRequest(BaseModel):
    farmer_id: int = Field(..., description="Unique Identifier for the farmer")
    user_name: str = Field(..., description="Name of the client")
    total_price: Optional[float] = Field(None, description="Total price for one order card")
    order_id: int = Field(None, description="Order ID for detailed view")
    page: Optional[int] = Field(1, ge=1, description="Page number for pagination (dashboard use)")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Number of records per page")

class FarmerOrderCardRequest(BaseModel):
    order_id: int = Field(..., description="Unique identifier for the order")
    order_date: datetime = Field(..., description="Date and time when the order was placed")
    buyer_id: int = Field(..., description="User id of the buyer")
    buyer_name: str = Field(..., description="Name of the buyer")
    total_amount: float = Field(..., description="Total price of the order items for the farmer")
    total_items: int = Field(..., description="Number of distinct products in the order")

class FarmerDashboardResponse(BaseModel):
    farmer_id: int = Field(..., description="Unique identifier for the farmer")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of records per page")
    total_orders: int = Field(..., description="Total number of orders available for that farmer")
    orders: List[FarmerOrderCardRequest] = Field(..., description="List of order cards for the farmer dashboard")

class OrderItemDetail(BaseModel):
    product_id: int = Field(..., description="Unique identifier for the product")
    product_name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., description="Quantity of the product ordered")
    unit_price: float = Field(..., description="Price unit of the product")
    total_price: float = Field(..., description="Total price for this product")

class OrderCardResponse(BaseModel):
    order_id: int = Field(..., description="Unique Identifier for the order")
    order_date: datetime = Field(..., description="Date and time when the order was placed")
    buyer_id: int = Field(..., description="Unique identifier for the buyer")
    buyer_name: str = Field(..., description="Name of the buyer")
    buyer_email: str = Field(..., description="Email of the buyer")
    total_amount: float = Field(..., description="Total amount for this order for the farmer")
    items: List[OrderItemDetail] = Field(..., description="List of products in this order for the farmer")
    