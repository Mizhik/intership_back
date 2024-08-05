from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.action import ActionDetail
from app.dtos.company import CompanyDetail, CompanySchema, CompanyUpdate
from app.dtos.user import UserDetail
from app.entity.models import User
from app.repository.action import ActionRepository
from app.repository.company import CompanyRepository
from app.services.action import ActionService
from app.services.auth import AuthService
from app.services.company import CompanyService
from app.services.user import UserService

router = APIRouter(prefix="/company", tags=["company"])


async def get_company_service(db: AsyncSession = Depends(get_db)):
    user_repository = CompanyRepository(db)
    action_repository = ActionRepository(db)
    return CompanyService(db, user_repository, action_repository)


@router.get("/", response_model=list[CompanyDetail])
async def get_companies(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    company_service=Depends(get_company_service),
):
    return await company_service.get_all_companies(offset, limit)


@router.get("/{company_id}", response_model=CompanyDetail)
async def get_company(company_id: UUID, company_service=Depends(get_company_service)):
    return await company_service.get_one_company(company_id)


@router.post("/", response_model=CompanyDetail)
async def create_company(
    body: CompanySchema,
    company_service=Depends(get_company_service),
    current_user: User = Depends(AuthService.get_current_user),
):
    return await company_service.create_company(body, current_user)


@router.put("/{company_id}", response_model=CompanyDetail)
async def update_company(
    company_id: UUID,
    body: CompanyUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    company_service=Depends(get_company_service),
):
    return await company_service.update_company(company_id, body, current_user)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    company_service=Depends(get_company_service),
    current_user: User = Depends(AuthService.get_current_user),
):
    return await company_service.delete_company(company_id, current_user)


# 13. Перегляд списку запрошених користувачів власником
@router.get("/companies/{company_id}/invitations", response_model=list[ActionDetail])
async def view_company_invitations(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service: CompanyService = Depends(get_company_service),
):
    return await action_service.get_company_invitations_to_users(
        company_id, current_user
    )


# 14. Перегляд списку запитів на приєднання власником
@router.get("/companies/{company_id}/requests", response_model=list[ActionDetail])
async def view_requests(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service: CompanyService = Depends(get_company_service),
):
    return await action_service.get_company_requests_to_users(company_id, current_user)


@router.get("/companies/{company_id}/members")
async def view_users_in_company(
    company_id: UUID,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    current_id: User = Depends(AuthService.get_current_user),
    action_service: UserService = Depends(get_company_service),
) -> list[UserDetail]:
    return await action_service.get_users_in_company(
        company_id,
        current_id,
        offset,
        limit,
    )
