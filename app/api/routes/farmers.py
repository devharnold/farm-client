from fastapi import APIRouter, Depends, HTTPException
from auth.password_utils import verify_password
from utils.token import create_access_token
from app.services.farmer_service import FarmerService
from app.schemas.farmers import RegisterRequest, FarmerLoginRequest, GetFarmerRequest
from app.db import get_db_pool

router = APIRouter()

@router.post("/")
async def register_farmer(req: RegisterRequest, db_pool=Depends(get_db_pool)):
    farmer_service = FarmerService(db_pool)
    return await farmer_service.register_farmer(
        email=req.email,
        password=req.password,
        username=req.username,
        role=req.role
    )

@router.post("/<int:farmer_id>/login")
def login(farmer: FarmerLoginRequest):
    try:
        farmer = FarmerService.farmer_login()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error{e}")
    return farmer


@router.get("/farmers/<string:email>")
async def get_farmer(req: GetFarmerRequest, db_pool=Depends(get_db_pool)):
    try:
        farmer_service = FarmerService(db_pool)
        return await farmer_service.get_farmer_by_email(
            email=req.email,
            username=req.username,
            farmer_id=req.farmer_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
