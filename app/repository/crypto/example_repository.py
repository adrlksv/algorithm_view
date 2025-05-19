# app/repositories/example_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.example.models import Example
from datetime import datetime


class ExampleRepository:
    @staticmethod
    async def create(
        session: AsyncSession,
        user_id: int,
        algorithm_id: int,
        key_id: int,
        input_data: str,
        output_data: str,
        params: dict
    ) -> Example:
        example = Example(
            user_id=user_id,
            algorithm_id=algorithm_id,
            key_id=key_id,
            input_data=input_data,
            output_data=output_data,
            parameters=params,
            notes="Auto-generated example",
            created_at=datetime.now(),
            is_favorite=False
        )
        session.add(example)
        await session.commit()
        await session.refresh(example)
        return example