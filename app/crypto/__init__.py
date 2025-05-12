from crypto.algorithms.aes.aes import AESAlgorithm
from crypto.algorithms.rsa.rsa import RSAAlgorithm
from crypto.algorithms.ecc.ecc import ECCAlgorithm

from crypto.algorithms.base import KeyAlgorithm


class AlgorithmFactory:
    @staticmethod
    def create(algorithm: str) -> 'KeyAlgorithm':
        algorithm = algorithm.lower()
        if algorithm == "aes":
            return AESAlgorithm()
        elif algorithm == "rsa":
            return RSAAlgorithm()
        elif algorithm == "ecc":
            return ECCAlgorithm()
        raise ValueError(f"Unsupported algorithm: {algorithm}")
