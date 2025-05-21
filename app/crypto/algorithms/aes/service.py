# app/services/aes_service.py
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from datetime import datetime


class AesService:
    @staticmethod
    def _pad(data: bytes) -> bytes:
        pad_len = 16 - (len(data) % 16)
        return data + bytes([pad_len] * pad_len)

    @staticmethod
    async def generate_key(key_size: int) -> tuple[str, str]:
        key = os.urandom(key_size // 8)
        iv = os.urandom(16)
        return key.hex(), iv.hex()

    @staticmethod
    async def encrypt(key: str, iv: str, data: str) -> str:
        cipher = Cipher(
            algorithms.AES(bytes.fromhex(key)),
            modes.CBC(bytes.fromhex(iv)),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        padded = AesService._pad(data.encode())
        encrypted = encryptor.update(padded) + encryptor.finalize()
        return encrypted.hex()
