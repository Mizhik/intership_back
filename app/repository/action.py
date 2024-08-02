from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from app.dtos.action import ActionDetail
from app.dtos.user import UserDetail
from app.entity.enums import ActionStatus
from app.repository.base_repository import BaseRepository
from app.entity.models import Action


class ActionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db=db, model=Action)

    async def get_requests(
        self, user_id: Optional[UUID] = None, company_id: Optional[UUID] = None
    ) -> List[ActionDetail]:
        stmt = select(self.model).filter_by(status=ActionStatus.REQUESTED_TO_JOIN)
        if user_id:
            stmt = stmt.filter_by(user_id=user_id)
        elif company_id:
            stmt = stmt.filter_by(company_id=company_id)
        else:
            raise ValueError("Either user_id or company_id must be provided")
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_invitations(
        self, user_id: Optional[UUID] = None, company_id: Optional[UUID] = None
    ) -> List[ActionDetail]:
        stmt = select(self.model).filter_by(status=ActionStatus.INVITED)
        if user_id:
            stmt = stmt.filter_by(user_id=user_id)
        elif company_id:
            stmt = stmt.filter_by(company_id=company_id)
        else:
            raise ValueError("Either user_id or company_id must be provided")
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_users_by_company(
        self,
        company_id: UUID,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[UserDetail]:
        stmt = select(self.model).filter_by(
            company_id=company_id, status=ActionStatus.MEMBER
        )
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        users = await self.db.execute(stmt)
        return users.scalars().all()
