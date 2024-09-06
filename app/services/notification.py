from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.models import User
from app.repository.notification import NotificationRepository
from app.services.errors import UserForbidden


class NotificationService:
    def __init__(self, db: AsyncSession, repository: NotificationRepository):
        self.db = db
        self.repository = repository

    async def get_all_notifications(self, user_id: UUID, current_user: User):
        if user_id != current_user.id:
            raise UserForbidden
        return await self.repository.get_notifications(user_id)

    async def read_notification(
        self, user_id: UUID, notification_id: UUID, current_user: User
    ):
        if user_id != current_user.id:
            raise UserForbidden
        notification = await self.repository.get_one_or_404(
            {"user_id": user_id, "id": notification_id}
        )
        return await self.repository.update(notification.id, {"status": True})

    async def get_unread_notification(self, user_id:UUID, current_user:User):
        if user_id != current_user.id:
            raise UserForbidden
        return await self.repository.get_unread_notification(user_id)
