from pydantic import BaseModel

from enum import Enum


class ECCCurveName(str, Enum):
    secp256r1 = "secp256r1"
    secp384r1 = "secp384r1"
    secp521r1 = "secp521r1"

class SECCKeyGenerate(BaseModel):
    curve_name: ECCCurveName = ECCCurveName.secp256r1


class SECCKeyResponse(BaseModel):
    key_id: int
    public_key: str
    private_key: str
    curve_name: str
