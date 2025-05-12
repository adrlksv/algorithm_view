import os

from typing import Dict

from crypto.algorithms.base import KeyAlgorithm


class AESAlgorithm(KeyAlgorithm):
    def generate_keys(self, **params) -> Dict[str, str]:
        key_size = params.get('key_size', 256)
        
        if key_size not in [128, 192, 256]:
            raise ValueError("Invalid AES key size. Must be 128, 192 or 256 bits.")
        key = os.urandom(key_size // 8)
        
        return {"key": key.hex()}
