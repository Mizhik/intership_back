from app.repository.base_repository import BaseRepository
from app.entity.models import Company


class CompanyRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Company)

