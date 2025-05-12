from crypto import AlgorithmFactory


class CryptoService:
    def generate_keys(self, algorithm: str, **params) -> dict:
        algo = AlgorithmFactory.create(algorithm)
        return algo.generate_keys(**params)
