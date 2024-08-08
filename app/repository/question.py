from app.repository.base_repository import BaseRepository
from app.entity.models import Question


class QuestionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Question)
