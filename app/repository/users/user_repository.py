from repository.base.base import BaseRepository
from db.users.models import User


class UsersRepository(BaseRepository):
    model = User
