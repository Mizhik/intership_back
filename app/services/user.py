from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.dtos.user import UserDetail, UserSchema, UserUpdate
from app.entity.models import User
from app.repository.users import UserRepository
from app.utils.hash_password import Hash
from app.services.errors import UserForbidden


class UserService:
    def __init__(self, db: AsyncSession, repository: UserRepository):
        self.db = db
        self.repository = repository

    async def get_all_users(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[UserDetail]:
        return await self.repository.get_many(offset, limit)

    async def get_one_user(self, user_id: UUID) -> UserDetail:
        return await self.repository.get_one_or_404({"id": user_id})

    async def create_user(self, body: UserSchema) -> UserDetail:
        body_dict = body.model_dump()
        body_dict["password"] = Hash.get_password_hash(body_dict["password"])
        user = await self.repository.create(body_dict)
        return user

    async def update_user(
        self, user_id: UUID, body: UserUpdate, current_user: User
    ) -> UserDetail:
        body_dict = body.model_dump()
        if user_id != current_user.id:
            raise UserForbidden

        if body_dict.get("password"):
            body_dict["password"] = Hash.get_password_hash(body_dict["password"])
        return await self.repository.update(user_id, body_dict)

    async def delete_user(self, user_id: UUID, current_user: User) -> None:
        if user_id != current_user.id:
            raise UserForbidden
        return await self.repository.delete_res(user_id)
