# app/repositories/key_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.key.models import Key
from datetime import datetime


class KeyRepository:
    @staticmethod
    async def create(
        session: AsyncSession, 
        algorithm_type: str,
        key_data: str,
        key_length: int
    ) -> Key:
        key = Key(
            algorithm_type=algorithm_type,
            key_data=key_data,
            key_length=key_length,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True
        )
        session.add(key)
        await session.commit()
        await session.refresh(key)
        return key
