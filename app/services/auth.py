from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.user import UserSchema
from app.entity.models import User
from app.repository.users import UserRepository
from app.services.user import UserService
from app.utils.auth import Auth
from app.utils.hash_password import Hash


security = HTTPBearer()


class AuthService:
    def __init__(self, db: AsyncSession, repository: UserRepository):
        self.db = db
        self.repository = repository

    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db),
    ):
        token = credentials.credentials
        email, token_source = await Auth.get_current_user_with_token(token)

        user = await db.execute(select(User).where(User.email == email))
        user = user.scalar_one_or_none()

        if user is None:
            if token_source == "own_service":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            elif token_source == "auth0":
                user = User(
                    username=email.split("@")[0],
                    email=email,
                    password=await Hash.get_password_hash(str(datetime.now())),
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)

        return user

    async def get_user_by_email(self, email: str):
        return await self.repository.get_one(email=email)

    async def signup(self, body: UserSchema):
        user = await self.get_user_by_email(email=body.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
            )
        body.password = await Hash.get_password_hash(body.password)
        user = User(**body.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, body: HTTPAuthorizationCredentials):
        user = await self.get_user_by_email(email=body.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
            )
        if not await Hash.verify_password(body.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )
        access_token = await Auth.create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
        }
