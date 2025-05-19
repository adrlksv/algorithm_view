# app/schemas/crypto/aes/schemas.py
from pydantic import BaseModel, Field
from typing import Optional


class SAESKeyGenerate(BaseModel):
    key_size: int = Field(128, ge=128, le=256, description="Key size in bits (128, 192, 256)")
    sample_text: str = Field(..., min_length=1, description="Sample text to encrypt")
    notes: Optional[str] = Field(None, description="Optional notes")

class SAESKeyResponse(BaseModel):
    key_id: int
    key_data: str
    example_id: int
    encrypted_sample: str
    iv: str

class SAESEncryptRequest(BaseModel):
    key_id: int = Field(..., description="ID of AES key to use")
    data: str = Field(..., min_length=1, description="Data to encrypt")
    iv: Optional[str] = Field(None, description="Initialization vector (16 bytes hex)")
    notes: Optional[str] = Field(None, description="Optional notes")

class SAESEncryptResponse(BaseModel):
    encrypted_data: str
    example_id: int
    iv: str

class SAESDecryptRequest(BaseModel):
    key_id: int = Field(..., description="ID of AES key to use")
    encrypted_data: str = Field(..., min_length=32, description="Encrypted data in hex format")
    notes: Optional[str] = Field(None, description="Optional notes")

class SAESDecryptResponse(BaseModel):
    decrypted_data: str
    example_id: int
