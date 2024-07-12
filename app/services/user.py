from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.users import UserRepository
from app.utils.hash_password import Hash
from logging_config import logger_decorator


class ErrorNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


class UserService:

    def __init__(self, db: AsyncSession, repository: UserRepository):
        self.db = db
        self.repository = repository

    @logger_decorator
    async def get_all_users(self, offset, limit):
        users = await self.repository.get_many(offset, limit)
        if not users:
            raise ErrorNotFound()
        return users

    @logger_decorator
    async def get_one_user(self, user_id):
        user = await self.repository.get_one(user_id)
        if not user:
            raise ErrorNotFound()
        return user

    @logger_decorator
    async def create_user(self, body):
        body.password = Hash.get_password_hash(body.password)
        user = await self.repository.create(body)
        return user

    @logger_decorator
    async def update_user(self, user_id, body):
        if body.password:
            body.password = Hash.get_password_hash(body.password)
        new_user = await self.repository.update(user_id, body)
        if not new_user:
            raise ErrorNotFound()
        return new_user

    @logger_decorator
    async def delete_user(self, user_id):
        user = await self.repository.delete_res(user_id)
        if not user:
            raise ErrorNotFound()
        return user
