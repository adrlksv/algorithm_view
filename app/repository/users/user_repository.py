from repository.base.base import BaseRepository
from app.db.users.models import User


class UsersRepository(BaseRepository):
    model = User
