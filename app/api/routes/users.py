from fastapi import APIRouter, HTTPException, Depends
from auth.password_utils import verify_password
from utils.token import create_access_token
from schemas import UserLogin
from app.db import get_db_pool
from app.schemas.user import RegisterRequest, LoginRequest, GetUserRequest
from app.services.user_service import UserService
from app.services.user_service import get_user_by_email

router = APIRouter()

@router.post("/")
async def register_farmer(req: RegisterRequest, db_pool=Depends(get_db_pool)):
    user_service = UserService(db_pool)
    return await user_service.register_user(
        email=req.email,
        password=req.password,
        username=req.username,
        role=req.role
    )

@router.post("/<int:user_id>/login")
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/<string:email>")
async def get_user(req: GetUserRequest, db_pool=Depends(get_db_pool)):
    user_service = UserService(db_pool)
    return await user_service.get_user_by_email(
        email=req.email,
        first_name=req.first_name,
        last_name=req.last_name
    )
