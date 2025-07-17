from fastapi import APIRouter, HTTPException, Depends
from app.db import get_db_pool
from app.schemas.product import AddProductRequest, ResetQuantityRequest, FindProductRequest, DeleteProductRequest
from app.services.product_service import ProductService

router = APIRouter()

@router.post("/")
async def create_product(req: AddProductRequest, db_pool=Depends(get_db_pool)):
    try: 
        product_service = ProductService(db_pool)
        return await product_service.add_products(
            farmer_id=req.farmer_id,
            product_name=req.product_name,
            product_category=req.product_category,
            product_quantity=req.product_quantity,
            product_price=req.product_price,
            product_id=req.product_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

@router.patch("/<int:product_quantity>")
async def reset_quantity(req: ResetQuantityRequest, db_pool=Depends(get_db_pool)):
    try:
        product_service = ProductService(db_pool)
        return await product_service.reset_product_quantity(
            product_id=req.product_id,
            product_quantity=req.product_quantity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
    
@router.delete("/<str:product_id>")
async def delete_product(req: DeleteProductRequest, db_pool=Depends(get_db_pool)):
    try:
        product_service = ProductService(db_pool)
        return await product_service.delete_product(
            product_id=req.product_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
    
@router.get("/products/<str:product_id>")
async def search_product(req: FindProductRequest, db_pool=Depends(get_db_pool)):
    try:
        product_service = ProductService(db_pool)
        return await product_service.check_if_product_exists(
            product_id=req.product_id,
            product_name=req.product_name,
            product_category=req.product_category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
    