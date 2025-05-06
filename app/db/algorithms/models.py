from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Algorithm(Base):
    __tablename__ = "algorithm"
    
    algorithm_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column
    key_lenghts: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
