# app/api/routers/aes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from crypto.algorithms.aes.service import AesService
from repository.crypto.example_repository import ExampleRepository
from repository.crypto.key_repository import KeyRepository


router = APIRouter(prefix="/aes", tags=["AES"])


@router.post("/generate")
async def generate_aes_key(
    key_size: int = 256,
    sample_text: str = "Test message",
    db: AsyncSession = Depends(get_db)
):
    try:
        # Генерация ключа
        key_hex, iv_hex = await AesService.generate_key(key_size)
        
        # Шифрование тестового сообщения
        encrypted = await AesService.encrypt(key_hex, iv_hex, sample_text)
        
        # Сохранение в БД
        key = await KeyRepository.create(
            db, "AES", f"{key_hex}:{iv_hex}", key_size
        )
        
        example = await ExampleRepository.create(
            db,
            user_id=1,  # В реальном приложении брать из авторизации
            algorithm_id=1,  # ID алгоритма AES из БД
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
