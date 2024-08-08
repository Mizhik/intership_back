from uuid import UUID
from app.repository.base_repository import BaseRepository
from app.entity.models import Answer, Question, Quiz


class QuizRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Quiz)
