from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.database import Base


class AlgorithmParameter(Base):
    __tablename__ = "algorithm_parameters"
    
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    algorithm_id: Mapped[int] = mapped_column(
        ForeignKey("algorithm.algorithm_id"), 
        nullable=False,
    )
    param_name: Mapped[str] = mapped_column(nullable=False)
    param_type: Mapped[str] = mapped_column(nullable=False)
    default_value: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
