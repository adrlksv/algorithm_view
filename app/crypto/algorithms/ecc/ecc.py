from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from typing import Dict

from crypto.algorithms.base import KeyAlgorithm


class ECCAlgorithm(KeyAlgorithm):
    CURVES = {
        "secp256r1": ec.SECP256R1,
        "secp384r1": ec.SECP384R1,
        "secp521r1": ec.SECP521R1,
    }

    def generate_keys(self, **params) -> Dict[str, str]:
        curve_name = params.get('curve_name', 'secp256r1')
        curve = self.CURVES.get(curve_name.lower(), ec.SECP256R1)()
        
        private_key = ec.generate_private_key(curve, default_backend())
        
        return {
            "private_key": private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode(),
            "public_key": private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }
