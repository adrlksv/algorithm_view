from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class AESMode(str, Enum):
    CBC = "CBC"
    ECB = "ECB"
    GCM = "GCM"


class SAESKeyGenerate(BaseModel):
    key_size: int = Field(..., ge=128, le=256, description="Размер ключа в битах")
    mode: AESMode = Field(default=AESMode.CBC, description="Режим работы AES")


class SAESKeyResponse(BaseModel):
    key_id: int
    key: str = Field(..., description="Сгенерированный ключ (hex)")
    iv: str | None = Field(None, description="Вектор инициализации (hex)")
    key_size: int
    mode: str
    created_at: datetime
