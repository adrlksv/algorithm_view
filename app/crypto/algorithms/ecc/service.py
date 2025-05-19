from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from typing import NamedTuple

import asyncio


class ECCKeyPair(NamedTuple):
    public_key: str
    private_key: str


class ECCKeyService:
    SUPPORTED_CURVES = {
        "secp256r1": ec.SECP256R1,
        "secp384r1": ec.SECP384R1,
        "secp521r1": ec.SECP521R1
    }

    @classmethod
    async def generate_key_pair(cls, curve_name: str = "secp256r1") -> ECCKeyPair:
        if curve_name not in cls.SUPPORTED_CURVES:
            raise ValueError(f"Unsupported curve. Supported: {list(cls.SUPPORTED_CURVES.keys())}")
        
        def _generate():
            private_key = ec.generate_private_key(cls.SUPPORTED_CURVES[curve_name]())
            
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            pub_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
            
            return ECCKeyPair(public_key=pub_pem, private_key=priv_pem)
        
        return await asyncio.to_thread(_generate)
