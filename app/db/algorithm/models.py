from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum

from app.db.database import Base

from enum import Enum


class AlgorithmType(str, Enum):
    AES = "AES"
    RSA = "RSA"
    ECC = "ECC"


class Algorithm(Base):
    __tablename__ = "algorithm"
    __table_args__ = {
        "extend_existing": True
    }
    
    algorithm_id: Mapped[int] = mapped_column(
        primary_key=True, 
        nullable=False, 
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(
        SQLAlchemyEnum(AlgorithmType), 
        nullable=False,
    )
    description: Mapped[str] = mapped_column(nullable=False)
    is_symmetric: Mapped[bool] = mapped_column(nullable=False)
