from fastapi import APIRouter, HTTPException, Depends
from app.schemas.product import ProductRequest, ProductRequestResponse
from app.services.product_service import ProductService

router = APIRouter()

@router.post("/")
async def create_product(req: ProductRequest)