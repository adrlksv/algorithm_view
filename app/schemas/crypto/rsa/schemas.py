from pydantic import BaseModel, Field
from typing import Annotated, Optional


class SRSAKeyGenerate(BaseModel):
    key_size: Annotated[int, Field(ge=2048, le=4096)]


class SRSAKeyResponse(BaseModel):
    key_id: int
    public_key: str
    private_key: str
    key_size: int


class SRSAEncryptRequest(BaseModel):
    key_id: int = Field(..., description="ID of RSA public key to use")
    data: str = Field(..., min_length=1, max_length=190, 
                     description="Data to encrypt (max 190 chars for RSA-2048)")
    notes: Optional[str] = Field(None, description="Optional notes for the example")

class SRSAEncryptResponse(BaseModel):
    encrypted_data: str = Field(..., description="Base64 encoded encrypted data")
    example_id: int = Field(..., description="ID of created example record")
    key_id: int = Field(..., description="ID of used key")
