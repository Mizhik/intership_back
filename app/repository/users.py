from app.repository.base_repository import BaseRepository
from app.entity.models import User


class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=User)
