from fastapi import APIRouter, Depends
from app.services.farmer_service import FarmerService
from app.schemas.farmers import RegisterRequest, LoginRequest
from app.db import get_db_pool

router = APIRouter()

@router.post("/register")
async def register_farmer(req: RegisterRequest, db_pool=Depends(get_db_pool)):
    farmer_service = FarmerService(db_pool)
    return await farmer_service.register_farmer(
        email=req.email,
        password=req.password,
        username=req.username,
        role=req.role
    )

@router.post("/login")
async def login_farmer(req: LoginRequest, db_pool=Depends(get_db_pool)):
    farmer_service = FarmerService(db_pool)
    return await farmer_service.farmer_login(
        
    )
