from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dtos.user import UserDetail, UserSchema
from app.repository.users import UserRepository
from app.utils.hash_password import Hash


class ErrorNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


class UserService:

    def __init__(self, db: AsyncSession, repository: UserRepository):
        self.db = db
        self.repository = repository

    async def get_all_users(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[UserDetail]:
        users = await self.repository.get_many(offset, limit)
        if not users:
            return []
        return users

    async def get_one_user(self, user_id: UUID) -> UserDetail:
        user = await self.repository.get_one(user_id)
        if not user:
            raise ErrorNotFound()
        return user

    async def create_user(self, body:UserSchema) -> UserDetail:
        body_dict = body.model_dump()
        body_dict["password"] = Hash.get_password_hash(body_dict["password"])
        user = await self.repository.create(body_dict)
        return user

    async def update_user(self, user_id: UUID, body: UserSchema) -> UserDetail:
        body_dict = body.model_dump()
        if body_dict.get("password"):
            body_dict["password"] = Hash.get_password_hash(body_dict["password"])
        new_user = await self.repository.update(user_id, body_dict)
        if not new_user:
            raise ErrorNotFound()
        return new_user

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.repository.delete_res(user_id)
        if not user:
            raise ErrorNotFound()
        return user
