from fastapi import APIRouter, Depends, HTTPException
from app.services.order_service import OrderService
from app.schemas.orders import PlaceOrderRequest, ViewCartRequest, ViewOrdersRequest
from app.db import get_db_pool

router = APIRouter()

# inject using FastAPI's depends
@router.post("/")
async def place_order(req: PlaceOrderRequest, db_pool=Depends(get_db_pool)):
    order_service = OrderService(db_pool)
    return await order_service.create_orders(
        user_id=req.user_id,
        product_id=req.product_id,
        farmer_id=req.farmer_id,
        unit_price=req.unit_price,
        total_price=req.total_price,
        created_at=req.created_at
    )

@router.get("/orders/view-cart")
async def view_cart(req: ViewCartRequest, db_pool=Depends(get_db_pool)):
    try:
        order_service = OrderService(db_pool)
        return await order_service.view_cart(
            product_id=req.product_id,
            product_quantity=req.product_quantity,
            unit_price=req.unit_price,
            total_price=req.total_price,
            date_created=req.date_created
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
    
@router.get('/orders/list-history')
async def list_order_history(req: ViewOrdersRequest, db_pool=Depends(get_db_pool)):
    try:
        order_service = OrderService(db_pool)
        return await order_service.view_orders(
            user_id=req.user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")

