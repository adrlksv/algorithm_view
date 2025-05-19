from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth_depends import get_current_user
from crypto.algorithms.aes.service import AESKeyService
from db.database import get_db
from db.users.models import User
from repository.crypto.key_repository import KeyRepository
from schemas.crypto.aes.schemas import SAESKeyGenerate, SAESKeyResponse


router = APIRouter(
    prefix="/aes",
    tags=["AES Keys"]
)


@router.post("/generate", response_model=SAESKeyResponse)
async def generate_aes_keys(
    request: SAESKeyGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        if not AESKeyService.validate_key_size(request.key_size):
            raise HTTPException(
                status_code=400,
                detail=f"Неподдерживаемый размер ключа. Допустимые: {AESKeyService.SUPPORTED_KEY_SIZES}"
            )
        
        return await AESKeyService.generate_and_store_keys(
            session=db,
            user_id=current_user.user_id,
            key_size=request.key_size,
            mode=request.mode
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка генерации ключей")
    

@router.get("/my-keys", response_model=list[SAESKeyResponse])
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
