from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth_depends import get_current_user
from crypto.algorithms.ecc.service import ECCKeyService
from db.database import get_db
from db.users.models import User
from repository.crypto.key_repository import KeyRepository
from schemas.crypto.ecc.schemas import SECCKeyGenerate, SECCKeyResponse


router = APIRouter(
    prefix="/crypto/ecc",
    tags=["ECC Keys"]
)


@router.post("/generate", response_model=SECCKeyResponse)
async def generate_ecc_keys(
    key_data: SECCKeyGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        key_pair = await ECCKeyService.generate_key_pair(key_data.curve_name)
        
        key_record = await KeyRepository.create_key(
            session=db,
            user_id=current_user.user_id,
            algorithm_type="ECC",
            public_key=key_pair.public_key,
            private_key=key_pair.private_key,
            key_size=key_data.curve_name.value
        )
        
        return {
            "key_id": key_record.id,
            "public_key": key_pair.public_key,
            "private_key": key_pair.private_key,
            "curve_name": key_data.curve_name.value
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/my-keys", response_model=list[SECCKeyResponse])
async def get_user_ecc_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    keys = await KeyRepository.get_user_keys(
        session=db,
        user_id=current_user.user_id,
        algorithm_type="ECC"
    )
    return keys
