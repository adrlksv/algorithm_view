from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.key.models import Key
from app.repository.crypto.base import BaseRepository

from typing import List, Optional


class KeyRepository(BaseRepository):
    model = Key

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        algorithm_type: str,
        key_data: str,
        key_length: int,
    ) -> Key:
        key = Key(
            algorithm_type=algorithm_type,
            key_data=key_data,
            key_length=key_length,
        )
        session.add(key)
        await session.commit()
        await session.refresh(key)
        return key

    @classmethod
    async def get_user_keys(
        cls,
        session: AsyncSession,
        user_id: int,
        algorithm_type: Optional[str] = None
    ) -> List[Key]:
        query = select(cls.model).where(cls.model.id == user_id)
        
        if algorithm_type:
            query = query.where(cls.model.algorithm_type == algorithm_type)
            
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_key_by_id(
        cls,
        session: AsyncSession,
        key_id: int,
        user_id: Optional[int] = None
    ) -> Optional[Key]:
        filters = [cls.model.id == key_id]
        if user_id:
            filters.append(cls.model.id == user_id)
            
        query = select(cls.model).where(and_(*filters))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def revoke_key(
        cls,
        session: AsyncSession,
        key_id: int,
        user_id: int
    ) -> bool:
        key = await cls.get_key_by_id(session, key_id, user_id)
        if not key:
            return False
            
        await session.delete(key)
        await session.commit()
        return True
