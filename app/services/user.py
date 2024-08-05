from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.dtos.action import ActionDetail
from app.dtos.user import UserDetail, UserSchema, UserUpdate
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.users import UserRepository
from app.utils.hash_password import Hash
from app.services.errors import UserForbidden


class UserService:
    def __init__(
        self,
        db: AsyncSession,
        repository: UserRepository,
        action_repository: ActionRepository,
    ):
        self.db = db
        self.repository = repository
        self.action_repository = action_repository

    async def get_all_users(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[UserDetail]:
        return await self.repository.get_many(offset, limit)

    async def get_one_user(self, user_id: UUID) -> UserDetail:
        return await self.repository.get_one_or_404({"id": user_id})

    async def create_user(self, body: UserSchema) -> UserDetail:
        body_dict = body.model_dump()
        body_dict["password"] = await Hash.get_password_hash(body_dict["password"])
        user = await self.repository.create(body_dict)
        return user

    async def update_user(
        self, user_id: UUID, body: UserUpdate, current_user: User
    ) -> UserDetail:
        body_dict = body.model_dump()
        if user_id != current_user.id:
            raise UserForbidden

        if body_dict.get("password"):
            body_dict["password"] = await Hash.get_password_hash(body_dict["password"])
        return await self.repository.update(user_id, body_dict)

    async def delete_user(self, user_id: UUID, current_user: User) -> None:
        if user_id != current_user.id:
            raise UserForbidden
        return await self.repository.delete_res(user_id)

    # general
    async def get_users_in_company(
        self,
        company_id: UUID,
        current_user: User,
        offset: Optional[int],
        limit: Optional[int],
    ) -> list[UserDetail]:
        await self.action_repository.is_user_owner(company_id, current_user.id)
        users = await self.action_repository.get_users_by_company(
            company_id, offset, limit
        )
        return users

    async def get_users_requests_to_companies(
        self, user_id: UUID
    ) -> list[ActionDetail]:
        return await self.action_repository.get_requests(user_id)

    async def get_users_invitations_from_companies(
        self, user_id: UUID
    ) -> list[ActionDetail]:
        return await self.action_repository.get_invitations(user_id)
