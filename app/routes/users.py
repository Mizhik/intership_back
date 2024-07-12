from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.user import UserDetail, UserSchema, UserUpdate
from app.repository.users import UserRepository
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


# для окремого сервіса
async def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return UserService(db, user_repository)


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
    user_id: UUID, body: UserUpdate, user_service=Depends(get_user_service)
):
    return await user_service.update_user(user_id, body)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, user_service=Depends(get_user_service)):
    return await user_service.delete_user(user_id)
