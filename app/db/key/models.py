from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum

from db.algorithm.models import AlgorithmType

from app.db.database import Base


class Key(Base):
    __tablename__ = "key"
    __table_args__ = {
        "extend_existing": True
    }
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    algorithm_type: Mapped[AlgorithmType] = mapped_column(
        SQLAlchemyEnum(AlgorithmType),
        nullable=False,
    )
    key_data: Mapped[str] = mapped_column(nullable=False)
    key_length: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    updated_at : Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
        nullable=False,
    )
