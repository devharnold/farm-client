from fastapi import APIRouter, HTTPException, Depends
from utils.password import verify_password
from utils.token import create_access_token
from schemas import UserLogin
from app.services.user_service import get_user_by_email

router = APIRouter()

@router.post("/login")
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
