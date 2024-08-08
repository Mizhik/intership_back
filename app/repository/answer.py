from app.repository.base_repository import BaseRepository
from app.entity.models import Answer


class AnswerRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Answer)
