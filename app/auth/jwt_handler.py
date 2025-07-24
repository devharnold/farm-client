import jwt
import os
import dotenv
from dotenv import load_dotenv
from fastapi import Request, HTTPException, Depends
from jwt import ExpiredSignatureError, InvalidTokenError 

load_dotenv()

SECRET_KEY = os.getenv("SECREET_KEY")
ALGORITHM = "HS256"

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")
    try:
        payload = jwt.decode(token[7:], SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # e.g. {'id': 1, 'username': 'john', 'role': 'farmer'}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")

def require_role(role: str):
    async def role_dependency(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return role_dependency
