from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.database import Base


class EduExample(Base):
    __tablename__ = "edu_example"
    
    example_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    input_data: Mapped[str] = mapped_column(nullable=False)
    algorithm_id: Mapped[int] = mapped_column(ForeignKey("algorithm.algorithm_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
