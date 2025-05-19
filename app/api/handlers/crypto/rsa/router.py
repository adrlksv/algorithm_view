from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repository.crypto.key_repository import KeyRepository
from app.crypto.algorithms.rsa.service import RSAKeyService
from app.schemas.crypto.rsa.schemas import SRSAKeyGenerate, SRSAKeyResponse
from api.dependencies.auth_depends import get_current_user
from app.db.users.models import User


router = APIRouter(
    prefix="/api/crypto/rsa",
    tags=["RSA Keys"]
)


@router.post("/generate", response_model=SRSAKeyResponse)
async def generate_rsa_keys(
    key_data: SRSAKeyGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        key_pair = await RSAKeyService.generate_key_pair(key_data.key_size)
        
        key_record = await KeyRepository.create_key(
            session=db,
            user_id=current_user.user_id,
            algorithm_type="RSA",
            key_data=key_pair.public_key,
            # private_key=key_pair.private_key,
            key_length=key_data.key_size
        )
        
        return {
            # "key_id": key_record.id,
            "public_key": key_pair.public_key,
            # "private_key": key_pair.private_key,
            "key_size": key_data.key_size
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/my-keys", response_model=list[SRSAKeyResponse])
async def get_user_rsa_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    keys = await KeyRepository.get_user_keys(
        session=db,
        user_id=current_user.user_id,
        algorithm_type="RSA"
    )
    return keys
