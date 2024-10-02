from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Annotated
from src.models.user import users
from src.utils.config import JWT_SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

def encode_token(payload: dict) -> str:
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    user = users.get(data["username"])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user