from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.user import UserDetail, UserSchema, UserLogin
from app.repository.users import UserRepository
from app.services.auth import AuthService
from app.dtos.auth import TokenSchema

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_auth_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return AuthService(db, user_repository)


@router.post("/signup", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, auth_service=Depends(get_auth_service)):
    return await auth_service.signup(body)


@router.post("/login", response_model=TokenSchema)
async def login(
    body: UserLogin,
    auth_service=Depends(get_auth_service),
):
    return await auth_service.login(body)


@router.get("/me", response_model=UserDetail)
async def user_me(current_user: UserDetail = Depends(AuthService.get_current_user)):
    return current_user
