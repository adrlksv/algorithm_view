from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repository.crypto.key_repository import KeyRepository
from app.crypto.algorithms.rsa.service import RSAKeyService
from app.schemas.crypto.rsa.schemas import SRSAKeyGenerate, SRSAKeyResponse
from api.dependencies.auth_depends import get_current_user
from app.db.users.models import User

import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/rsa",
    tags=["RSA Keys"]
)


@router.post("/generate", response_model=SRSAKeyResponse)
async def generate_rsa_keys(
    request: SRSAKeyGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Generating RSA keys for user {current_user.user_id}")
        # 1. Генерация ключей
        keys = await RSAKeyService.generate_keys(request.key_size)
        logger.debug(f"Generated keys: {keys.keys()}")  # Логируем только ключи без значений
        
        # 2. Сохранение в БД (оба ключа в key_data как JSON)
        key_record = await RSAKeyService.create_key_record(
            session=db,
            key_size=request.key_size,
            keys=keys
        )
        logger.info(f"Key record created: {key_record.id}")
        
        # 3. Возврат клиенту
        return SRSAKeyResponse(
            key_id=key_record.id,
            public_key=keys["public_key"],
            private_key=keys["private_key"],
            key_size=request.key_size,
            created_at=key_record.created_at
        )
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
