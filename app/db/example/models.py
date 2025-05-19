from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, JSON

from app.db.database import Base


class Example(Base):
    __tablename__ = "example"
    __table_args__ = {
        "extend_existing": True
    }
    
    example_id: Mapped[int] = mapped_column(
        primary_key=True, 
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"),
        nullable=False,
        index=True,
    )
    algorithm_id: Mapped[int] = mapped_column(
        ForeignKey("algorithm.algorithm_id"),
        nullable=False,
    )
    key_id: Mapped[int] = mapped_column(
        ForeignKey("key.id"),
        nullable=False,
    )
    input_data: Mapped[str] = mapped_column(nullable=False)
    output_data: Mapped[str] = mapped_column()
    parameters: Mapped[dict] = mapped_column(JSON)
    notes: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow(),
    )
    is_favorite: Mapped[bool] = mapped_column(default=False)
