from fastapi import APIRouter, Depends
from app.services.order_service import OrderService
#from app.schemas.orders import 
from app.db import get_db_pool

router = APIRouter()

# inject using FastAPI's depends
@router.post("/orders")
async def place_order(order_id: str, db_pool=Depends(get_db_pool)):
    service = OrderService(db_pool)
    return await service.create_multi_product_order(...)

@router.get("/<int:product_id>/products/")
async def get_product(product_id: int, db_pool = Depends(get_db_pool)):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM products WHERE id=$1", product_id)
        return dict(row)