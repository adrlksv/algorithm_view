from pydantic import BaseModel, Field
from typing import Annotated


class SRSAKeyGenerate(BaseModel):
    key_size: Annotated[int, Field(ge=2048, le=4096)]


class SRSAKeyResponse(BaseModel):
    key_id: int
    public_key: str
    private_key: str
    key_size: int
