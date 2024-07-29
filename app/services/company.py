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

    async def get_all_companies(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[CompanyDetail]:
        return await self.repository.get_many(offset, limit)    

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
        self, user_id: UUID, company_id: UUID, body: CompanyUpdate, current_user: User
    ) -> CompanyDetail:
        body_dict = body.model_dump()
        if user_id != current_user.id:
            raise UserForbidden

        return await self.repository.update(company_id, body_dict)

    async def delete_company(self, user_id:UUID ,company_id: UUID, current_user: User) -> None:
        if user_id != current_user.id:
            raise UserForbidden
        return await self.repository.delete_res(company_id)