from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from typing import NamedTuple
import asyncio


class RSAKeyPair(NamedTuple):
    public_key: str
    private_key: str


class RSAKeyService:
    SUPPORTED_KEY_SIZES = [2048, 3072, 4096]

    @classmethod
    async def generate_key_pair(cls, key_size: int) -> RSAKeyPair:
        if key_size not in cls.SUPPORTED_KEY_SIZES:
            raise ValueError(f"Unsupported key size. Supported: {cls.SUPPORTED_KEY_SIZES}")
        
        def _generate():
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            pub_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
            
            return RSAKeyPair(public_key=pub_pem, private_key=priv_pem)
        
        return await asyncio.to_thread(_generate)
