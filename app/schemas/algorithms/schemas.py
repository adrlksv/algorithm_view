from pydantic import BaseModel, Field, field_validator

from typing import Optional


class BaseKeyGenRequest(BaseModel):
    algorithm: str = Field(..., description="Algorithm type (aes, rsa, ecc)")


class AESKeyGenRequest(BaseKeyGenRequest):
    key_size: int = Field(256, description="Key size in bits (128, 192, 256)")

    @field_validator('key_size')
    def validate_key_size(cls, v):
        if v not in [128, 192, 256]:
            raise ValueError("AES key size must be 128, 192 or 256 bits")
        return v


class RSAKeyGenRequest(BaseKeyGenRequest):
    key_size: int = Field(2048, description="Key size in bits (>=1024)")

    @field_validator('key_size')
    def validate_key_size(cls, v):
        if v < 1024:
            raise ValueError("RSA key size must be at least 1024 bits")
        return v


class ECCKeyGenRequest(BaseKeyGenRequest):
    curve_name: str = Field("secp256r1", description="ECC curve name")


class KeyGenResponse(BaseModel):
    success: bool = True
    algorithm: str
    result: dict
