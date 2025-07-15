from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductRequest(BaseModel):
    product_id: str
    product_name: str

class ProductRequestResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: str
