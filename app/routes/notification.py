from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.dtos.notification import NotificationResponse
from app.entity.models import User
from app.repository.notification import NotificationRepository
from app.services.auth import AuthService
from app.services.notification import NotificationService


router = APIRouter(prefix="/notification", tags=["notification"])


async def get_notification_service(db: AsyncSession = Depends(get_db)):
    notification_repository = NotificationRepository(db)
    return NotificationService(db, notification_repository)


@router.get("/all", response_model=list[NotificationResponse])
async def get_all_notifications_user(
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return await notification_service.get_all_notifications(user_id, current_user)


@router.get("/unread", response_model=list[NotificationResponse])
async def get_unread_notification_user(
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return await notification_service.get_unread_notification(user_id, current_user)


@router.put("/read", response_model=NotificationResponse)
async def read_notification_user(
    user_id: UUID,
    notification_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    notification_service: NotificationService = Depends(get_notification_service),
):
    return await notification_service.read_notification(
        user_id, notification_id, current_user
    )
