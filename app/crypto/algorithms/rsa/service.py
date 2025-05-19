from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import asyncio
from datetime import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession

from db.key.models import Key
from repository.crypto.key_repository import KeyRepository


class RSAKeyService:
    SUPPORTED_KEY_SIZES = [2048, 3072, 4096]

    @classmethod
    def validate_key_size(cls, key_size: int) -> bool:
        return key_size in cls.SUPPORTED_KEY_SIZES

    @classmethod
    async def generate_keys(cls, key_size: int) -> dict:
        """Генерирует и возвращает оба ключа в словаре"""
        if not cls.validate_key_size(key_size):
            raise ValueError(f"Unsupported key size. Supported: {cls.SUPPORTED_KEY_SIZES}")
        
        def _generate():
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            
            # Сериализация ключей
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            pub_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
            
            return {
                "private_key": priv_pem,
                "public_key": pub_pem
            }
        
        return await asyncio.to_thread(_generate)

    @classmethod
    async def create_key_record(
        cls,
        session: AsyncSession,
        key_size: int,
        keys: dict  # {private_key, public_key}
    ) -> Key:
        """Сохраняет оба ключа в key_data как JSON строку"""
        
        key_record = await KeyRepository.create(
            session=session,
            algorithm_type="RSA",
            key_data=json.dumps(keys),  # Сохраняем оба ключа как JSON
            key_length=key_size,
        )
        return key_record
