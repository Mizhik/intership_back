from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.action import ActionDetail
from app.dtos.user import UserDetail, UserSchema, UserUpdate
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.users import UserRepository
from app.services.auth import AuthService
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


async def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    action_repository = ActionRepository(db)
    return UserService(db, user_repository, action_repository)


# 11. Перегляд запитів на приєднання користувачем
@router.get("/requests", response_model=list[ActionDetail])
async def view_user_requests(
    current_user: User = Depends(AuthService.get_current_user),
    action_service: UserService = Depends(get_user_service),
):
    return await action_service.get_users_requests_to_companies(current_user.id)


# 12. Перегляд запрошень користувачем
@router.get("/invitations", response_model=list[ActionDetail])
async def view_user_invitations(
    current_user: User = Depends(AuthService.get_current_user),
    action_service: UserService = Depends(get_user_service),
):
    return await action_service.get_users_invitations_from_companies(current_user.id)


@router.get("/", response_model=list[UserDetail])
async def get_users(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    user_service=Depends(get_user_service),
):
    return await user_service.get_all_users(offset, limit)


@router.get("/{user_id}", response_model=UserDetail)
async def get_user(user_id: UUID, user_service=Depends(get_user_service)):
    return await user_service.get_one_user(user_id)


@router.post("/", response_model=UserDetail)
async def create_user(body: UserSchema, user_service=Depends(get_user_service)):
    return await user_service.create_user(body)


@router.put("/{user_id}", response_model=UserDetail)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    user_service=Depends(get_user_service),
):
    return await user_service.update_user(user_id, body, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_service=Depends(get_user_service),
    current_user: User = Depends(AuthService.get_current_user),
):
    return await user_service.delete_user(user_id, current_user)