from abc import ABC, abstractmethod

from typing import Dict, Any


class KeyAlgorithm(ABC):
    @abstractmethod
    def generate_keys(self, **params) -> Dict[str, Any]:
        pass
