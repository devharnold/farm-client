from pydantic import BaseModel, EmailStr


class ProductRequest(BaseModel):
    product_id: str
    