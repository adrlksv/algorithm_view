# app/services/rsa_service.py
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class RsaService:
    @staticmethod
    async def generate_key(key_size: int) -> tuple[str, str]:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        priv_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        pub_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        return priv_pem, pub_pem
