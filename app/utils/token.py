import jwt
from app.services.user_service import UserService
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data: dict, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode = {"sub": str(user_id), "exp": expire, "iat": datetime.now(timezone.utc)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str) -> dict | None:
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_payload
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except InvalidTokenError:
        print("Invalid Token")
        return None