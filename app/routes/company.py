from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.company import CompanyDetail, CompanySchema, CompanyUpdate
from app.entity.models import User
from app.repository.company import CompanyRepository
from app.services.auth import AuthService
from app.services.company import CompanyService

router = APIRouter(prefix="/company", tags=["company"])


async def get_company_service(db: AsyncSession = Depends(get_db)):
    user_repository = CompanyRepository(db)
    return CompanyService(db, user_repository)


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
    user_id:UUID,
    company_id: UUID,
    body: CompanyUpdate,
    current_user: User = Depends(AuthService.get_current_user),
    company_service=Depends(get_company_service),
):
    return await company_service.update_company(user_id, company_id, body, current_user)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    company_id: UUID,
    company_service=Depends(get_company_service),
    current_user: User = Depends(AuthService.get_current_user),
):
    return await company_service.delete_company(user_id, company_id, current_user)
