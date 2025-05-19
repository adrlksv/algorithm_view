from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

from datetime import datetime

class User(Base):
    __tablename__ = "user"
    __table_args__ = {
        "extend_existing": True
    }
    
    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, 
        default=datetime.utcnow(),
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
