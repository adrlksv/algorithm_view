import os
from typing import NamedTuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import asyncio
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from repository.crypto.key_repository import KeyRepository
from schemas.crypto.aes.schemas import SAESKeyResponse  


class AESKeyPair(NamedTuple):
    key: str
    iv: str | None

class AESKeyService:
    SUPPORTED_KEY_SIZES = [128, 192, 256]  # В битах
    
    @classmethod
    def validate_key_size(cls, key_size: int) -> bool:
        return key_size in cls.SUPPORTED_KEY_SIZES

    @classmethod
    async def generate_key_pair(cls, key_size: int) -> AESKeyPair:
        """
        Генерирует AES ключ и IV (вектор инициализации)
        Возвращает hex-строки
        """
        if not cls.validate_key_size(key_size):
            raise ValueError(f"Неподдерживаемый размер ключа. Допустимые: {cls.SUPPORTED_KEY_SIZES}")

        def _generate():
            key = os.urandom(key_size // 8)
            iv = os.urandom(16)  # 128 бит для AES-CBC
            return AESKeyPair(key=key.hex(), iv=iv.hex())

        return await asyncio.to_thread(_generate)

    @classmethod
    async def generate_and_store_keys(
        cls,
        session: AsyncSession,
        user_id: int,
        key_size: int,
        mode: str = "CBC"
    ) -> SAESKeyResponse:
        """
        Полный цикл: генерация + сохранение в БД + логирование
        """
        # Генерация ключей
        key_pair = await cls.generate_key_pair(key_size)
        
        # Сохранение в БД
        key_record = await KeyRepository.create_key(
            session=session,
            user_id=user_id,
            algorithm_type="AES",
            public_key=key_pair.key,
            private_key=key_pair.iv,  # Храним IV как "приватный" ключ
            key_size=key_size,
            additional_params={"mode": mode}
        )
        
        return SAESKeyResponse(
            key_id=key_record.id,
            key=key_pair.key,
            iv=key_pair.iv,
            key_size=key_size,
            mode=mode,
            created_at=datetime.utcnow()
        )

    @classmethod
    async def encrypt_data(
        cls,
        key: str,
        iv: str | None,
        data: bytes,
        mode: str = "CBC"
    ) -> bytes:
        """
        Шифрование данных сгенерированным ключом
        """
        def _encrypt():
            backend = default_backend()
            key_bytes = bytes.fromhex(key)
            
            if mode == "CBC":
                iv_bytes = bytes.fromhex(iv) if iv else None
                cipher = Cipher(
                    algorithms.AES(key_bytes),
                    modes.CBC(iv_bytes),
                    backend=backend
                )
            elif mode == "ECB":
                cipher = Cipher(
                    algorithms.AES(key_bytes),
                    modes.ECB(),
                    backend=backend
                )
            else:
                raise ValueError("Unsupported AES mode")
            
            encryptor = cipher.encryptor()
            return encryptor.update(data) + encryptor.finalize()

        return await asyncio.to_thread(_encrypt)
