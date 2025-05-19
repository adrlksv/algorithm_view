# app/api/routers/ecc.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from crypto.algorithms.ecc.service import EccService
from repository.crypto.example_repository import ExampleRepository
from repository.crypto.key_repository import KeyRepository


router = APIRouter(prefix="/ecc", tags=["ECC"])

@router.post("/generate")
async def generate_ecc_key(
    curve_name: str = "secp256r1",
    db: AsyncSession = Depends(get_db)
):
    try:
        priv_pem, pub_pem = await EccService.generate_key(curve_name)
        
        key = await KeyRepository.create(
            db, "ECC", f"{priv_pem}||{pub_pem}", len(curve_name)
        )
        
        example = await ExampleRepository.create(
            db,
            user_id=1,
            algorithm_id=3,  # ID алгоритма ECC из БД
            key_id=key.id,
            input_data="Key generation",
            output_data="ECC key pair created",
            params={"curve": curve_name}
        )
        
        return {
            "key_id": key.id,
            "example_id": example.example_id,
            "private_key": priv_pem,
            "public_key": pub_pem
        }
    except Exception as e:
        raise HTTPException(500, str(e))
