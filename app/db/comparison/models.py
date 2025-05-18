from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, JSON

from app.db.database import Base


class Comparison(Base):
    __tablename__ = "comparison"
    
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"),
        nullable=False,
    )
    algorithm1_id: Mapped[int] = mapped_column(ForeignKey("algorithm.algorithm_id"))
    algorithm2_id: Mapped[int] = mapped_column(ForeignKey("algorithm.algorithm_id"))
    input_data: Mapped[str] = mapped_column(nullable=False)
    results: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow(),
    )
