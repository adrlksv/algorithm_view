from typing import Union
from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.auth_depends import get_current_user
from app.crypto.crypto_service import CryptoService
from app.schemas.algorithms.schemas import (
    AESKeyGenRequest, RSAKeyGenRequest, ECCKeyGenRequest, KeyGenResponse
)
from db.users.models import User


router = APIRouter(
    prefix="/generate-keys",
    tags=["Generate keys"],
)

RequestTypes = Union[AESKeyGenRequest, RSAKeyGenRequest, ECCKeyGenRequest]

@router.post("/", response_model=KeyGenResponse)
async def generate_keys(
    request: RequestTypes,
    current_user: User = Depends(get_current_user)
):
    try:
        params = request.dict(exclude={"algorithm"})
        
        result = CryptoService.generate_keys(
            algorithm=request.algorithm,
            **params
        )
        
        return KeyGenResponse(
            algorithm=request.algorithm,
            result=result
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Key generation failed: {str(e)}"
        )
