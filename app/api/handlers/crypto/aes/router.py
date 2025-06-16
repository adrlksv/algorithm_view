from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_depends import get_current_user
from app.db.database import get_db

from app.crypto.algorithms.aes.service import AesService

from app.repository.crypto.example_repository import ExampleRepository
from app.repository.crypto.key_repository import KeyRepository
from app.db.users.models import User


router = APIRouter(prefix="/aes", tags=["AES"])


@router.post("/generate")
async def generate_aes_key(
    key_size: int = 256,
    sample_text: str = "Test message",
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        key_hex, iv_hex = await AesService.generate_key(key_size)
        
        encrypted = await AesService.encrypt(key_hex, iv_hex, sample_text)
        
        key = await KeyRepository.create(
            db, "AES", f"{key_hex}:{iv_hex}", key_size
        )
        
        example = await ExampleRepository.create(
            db,
            user_id=user.user_id,
            algorithm_id=1,
            key_id=key.id,
            input_data=sample_text,
            output_data=encrypted,
            params={
                "key_size": key_size,
                "mode": "CBC",
                "iv": iv_hex
            }
        )
        
        return {
            "key_id": key.id,
            "example_id": example.example_id,
            "key": key_hex,
            "iv": iv_hex,
            "encrypted_sample": encrypted
        }
    except Exception as e:
        raise HTTPException(500, str(e))
