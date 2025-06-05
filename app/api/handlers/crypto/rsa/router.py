# app/api/routers/rsa.py
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth_depends import get_current_user
from app.db.database import get_db

from app.crypto.algorithms.rsa.service import RsaService

from app.repository.crypto.example_repository import ExampleRepository
from app.repository.crypto.key_repository import KeyRepository
from app.db.users.models import User


router = APIRouter(prefix="/rsa", tags=["RSA"])


@router.post("/generate")
async def generate_rsa_key(
    key_size: int = 2048,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        priv_pem, pub_pem = await RsaService.generate_key(key_size)
        
        key = await KeyRepository.create(
            db, "RSA", f"{priv_pem}||{pub_pem}", key_size
        )
        
        example = await ExampleRepository.create(
            db,
            user_id=user.user_id,
            algorithm_id=2,  # ID алгоритма RSA из БД
            key_id=key.id,
            input_data="Key generation",
            output_data="RSA key pair created",
            params={"key_size": key_size}
        )
        
        return {
            "key_id": key.id,
            "example_id": example.example_id,
            "private_key": priv_pem,
            "public_key": pub_pem
        }
    except Exception as e:
        raise HTTPException(500, str(e))
