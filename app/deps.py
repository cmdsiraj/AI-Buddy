# deps.py
from fastapi import Request, HTTPException
from jose import JWTError
from .utils.auth_utils import decode_token

def current_user(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=303, headers={"Location": "/auth/login"})
    try:
        payload = decode_token(token)
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=303, headers={"Location": "/auth/login"})
