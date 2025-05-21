# app/middlewares/auth.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer

from services.auth.jwt.jwt_auth import decode_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        
        token = credentials.credentials
        payload = decode_token(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid token or expired")
        
        return payload