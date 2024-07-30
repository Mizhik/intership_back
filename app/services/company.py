from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.company import CompanyDetail, CompanySchema, CompanyUpdate
from app.entity.models import User
from app.repository.company import CompanyRepository
from app.services.errors import UserForbidden

class CompanyService:

    def __init__(self, db: AsyncSession, repository: CompanyRepository):
        self.db = db
        self.repository = repository

    async def check_owner_and_get_company(
        self, company_id: UUID, current_user: User  
    ) -> CompanyDetail:
        company = await self.repository.get_one_or_404({"id": company_id})
        if company.owner_id != current_user.id:
            raise UserForbidden 
        return company

    async def get_all_companies(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CompanyDetail]:
        return await self.repository.get_many_with_is_visible(offset, limit)

    async def get_one_company(self, company_id: UUID) -> CompanyDetail:
        return await self.repository.get_one_or_404({"id": company_id})

    async def create_company(
        self, body: CompanySchema, current_user: User
    ) -> CompanyDetail:
        body_dict = body.model_dump()
        body_dict["owner_id"] = current_user.id
        company = await self.repository.create(body_dict)
        return company

    async def update_company(
        self, company_id: UUID, body: CompanyUpdate, current_user: User
    ) -> CompanyDetail:
        await self.check_owner_and_get_company(company_id, current_user)
        return await self.repository.update(company_id, body.model_dump())

    async def delete_company(self, company_id: UUID, current_user: User) -> None:
        await self.check_owner_and_get_company(company_id, current_user)
        return await self.repository.delete_res(company_id)
