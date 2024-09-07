from uuid import UUID

from sqlalchemy import select
from app.repository.base_repository import BaseRepository
from app.entity.models import Notification


class NotificationRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Notification)

    async def get_notifications(self, user_id: UUID):
        stmt = select(self.model).filter(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_unread_notification(self, user_id: UUID):
        stmt = select(self.model).filter(self.model.user_id == user_id, self.model.status == False)
        result = await self.db.execute(stmt)
        return result.scalars().all()
