# dashboard route

from fastapi import APIRouter, Depends, HTTPException
from app.services.farmer_dashboard import FarmerDashboard
from app.schemas.dashboard import FarmerDashboardRequest, FarmerDashboardResponse, OrderCardResponse
from typing import Optional

router = APIRouter()

@router.get("dashboard", response_model=FarmerDashboardResponse)
async def get_dashboard(req: FarmerDashboardRequest, farmer_id: int, page: Optional[int] = 1, limit: Optional[int] = 10, dashboard_service: FarmerDashboard = Depends()):
    # Get paginated list of orders for the farmer dashboard view
    return await dashboard_service.get_dashboard_summary(
        farmer_id=farmer_id,
        page=page,
        limit=limit
    )

# single order detail route
router.get("/orders/{order_id}", response_model=OrderCardResponse)
async def get_order_detail(order_id: int, farmer_id: int, dashboard_service: FarmerDashboard = Depends()):
    return await dashboard_service.get_order_details(
        order_id=order_id,
        farmer_id=farmer_id
    )