# app/schemas/crypto/ecc/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

ECCCurveType = Literal["secp256r1", "secp384r1", "secp521r1"]

class SECCKeyGenerate(BaseModel):
    curve_name: ECCCurveType = Field(..., description="ECC curve name")
    notes: Optional[str] = Field(None, description="Optional notes")

class SECCKeyResponse(BaseModel):
    key_id: int
    public_key: str
    private_key: str
    curve_name: str
    example_id: int
    created_at: datetime

class SECCSignRequest(BaseModel):
    key_id: int = Field(..., description="ID of ECC private key to use")
    data: str = Field(..., min_length=1, description="Data to sign")
    notes: Optional[str] = Field(None, description="Optional notes")

class SECCSignResponse(BaseModel):
    signature: str
    example_id: int
    key_id: int

class SECCVerifyRequest(BaseModel):
    key_id: int = Field(..., description="ID of ECC public key to use")
    data: str = Field(..., min_length=1, description="Original data")
    signature: str = Field(..., min_length=1, description="Signature to verify")
    notes: Optional[str] = Field(None, description="Optional notes")

class SECCVerifyResponse(BaseModel):
    is_valid: bool
    example_id: int
    key_id: int
