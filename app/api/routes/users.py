from fastapi import APIRouter, HTTPException, Depends
from utils.token import create_access_token
from app.db import get_db_pool
from app.schemas.user import UserRegisterRequest, LoginRequest, GetUserRequest
from app.services.user_service import UserService

router = APIRouter()

@router.post("/")
async def regsiter_user(req: UserRegisterRequest, db_pool=Depends(get_db_pool)):
    user_service = UserService(db_pool)
    return await user_service.register_user(
        email=req.email,
        password=req.password,
        username=req.username,
        phone=req.phone,
        role=req.role,
        created_at=req.created_at
    )

@router.post("/<int:user_id>/login")
def login(req: LoginRequest):
    try:
        user = UserService.user_login(
            email=req.email,
            password=req.password
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")
    return user


@router.get("/users/<string:email>")
async def get_user(req: GetUserRequest, db_pool=Depends(get_db_pool)):
    try:
        user_service = UserService(db_pool)
        return await user_service.get_user_by_email(
            email=req.email
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error {e}")