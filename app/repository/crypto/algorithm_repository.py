from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.algorithm.models import Algorithm
from app.repository.crypto.base import BaseRepository

from typing import List, Optional


class AlgorithmRepository(BaseRepository):
    model = Algorithm

    @classmethod
    async def get_algorithm_by_name(
        cls,
        session: AsyncSession,
        name: str
    ) -> Optional[Algorithm]:
        return await cls.find_one_or_none(session, name=name)

    @classmethod
    async def get_all_algorithms(
        cls,
        session: AsyncSession
    ) -> List[Algorithm]:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_supported_key_sizes(
        cls,
        session: AsyncSession,
        algorithm_name: str
    ) -> List[int]:
        algorithm = await cls.get_algorithm_by_name(session, algorithm_name)
        if not algorithm:
            return []
            
        return [int(size) for size in algorithm.supported_key_sizes.split(',')]
