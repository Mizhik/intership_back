from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.action import ActionDetail
from app.dtos.user import UserDetail
from app.entity.enums import ActionStatus
from app.entity.models import Action, User
from app.repository.action import ActionRepository
from app.services.errors import ErrorNotFound, UserForbidden

# TODO: add func for checking status(case)


class ActionService:

    def __init__(self, db: AsyncSession, repository: ActionRepository):
        self.db = db
        self.repository = repository

    @staticmethod
    async def is_user_owner(company_id: UUID, user_id: UUID, db: AsyncSession):
        stmt = select(Action).filter_by(
            company_id=company_id, user_id=user_id, status=ActionStatus.OWNER
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_action(body: dict, db: AsyncSession):
        action = Action(**body)
        db.add(action)
        await db.commit()
        await db.refresh(action)
        return action

    async def update_status(self, action: Action, status: ActionStatus):
        action.status = status
        await self.db.commit()
        await self.db.refresh(action)
        return action

    # C to U
    async def send_invitation(
        self, company_id: UUID, user_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden

        user_action = await self.repository.get_one(
            user_id=user_id, company_id=company_id
        )

        if not user_action:
            action = dict(
                user_id=user_id, company_id=company_id, status=ActionStatus.INVITED
            )
            return await self.repository.create(action)

        status_to_message = {
            ActionStatus.MEMBER: "Already member",
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.INVITED: "Already invited",
            ActionStatus.INVITATION_CANCELLED: "Already cancelled",
            ActionStatus.INVITATION_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if user_action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[user_action.status],
            )

    async def cancel_invitation(
        self, company_id: UUID, invitation_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden

        action = await self.repository.get_one_or_404(
            {"id": invitation_id, "company_id": company_id}
        )
        status_to_message = {
            ActionStatus.INVITATION_CANCELLED: "Already cancelled",
            ActionStatus.INVITATION_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.INVITATION_CANCELLED)

    async def accept_invitation(
        self, company_id: UUID, invitation_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden
        action = await self.repository.get_one_or_404(
            {"id": invitation_id, "company_id": company_id}
        )
        status_to_message = {
            ActionStatus.MEMBER: "Already member",
            ActionStatus.INVITATION_CANCELLED: "Already cancelled",
            ActionStatus.INVITATION_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.MEMBER)

    async def decline_invitation(
        self, company_id: UUID, invitation_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden
        action = await self.repository.get_one_or_404(
            {"id": invitation_id, "company_id": company_id}
        )
        status_to_message = {
            ActionStatus.INVITATION_CANCELLED: "Already cancelled",
            ActionStatus.INVITATION_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.INVITATION_DECLINED)

    async def get_company_invitations_to_users(
        self, company_id: UUID, current_user: User
    ) -> list[ActionDetail]:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden
        return await self.repository.get_invitations(company_id)

    async def get_company_requests_to_users(
        self, company_id: UUID, current_user: User
    ) -> list[ActionDetail]:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden
        return await self.repository.get_requests(company_id)

    # U to C
    async def request_to_join(
        self, company_id: UUID, current_user: User
    ) -> ActionDetail:
        user_action = await self.repository.get_one(
            company_id=company_id, user_id=current_user.id
        )
        if not user_action:
            action = dict(
                user_id=current_user.id,
                company_id=company_id,
                status=ActionStatus.REQUESTED_TO_JOIN,
            )
            return await self.repository.create(action)

        status_to_message = {
            ActionStatus.REQUESTED_TO_JOIN: "Already requested to join",
            ActionStatus.MEMBER: "Already member",
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.INVITED: "Already invited",
            ActionStatus.REQUEST_CANCELLED: "Already cancelled",
            ActionStatus.REQUEST_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if user_action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[user_action.status],
            )

    async def cancel_request(
        self, request_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404(
            {"id": request_id, "user_id": current_user.id}
        )
        status_to_message = {
            ActionStatus.MEMBER: "Already member",
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.REQUEST_CANCELLED: "Already cancelled",
            ActionStatus.REQUEST_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.REQUEST_CANCELLED)

    async def accept_request(
        self, request_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404(
            {"id": request_id, "user_id": current_user.id}
        )
        status_to_message = {
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.REQUEST_CANCELLED: "Already cancelled",
            ActionStatus.REQUEST_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.MEMBER)

    async def decline_request(
        self, request_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404(
            {"id": request_id, "user_id": current_user.id}
        )
        status_to_message = {
            ActionStatus.MEMBER: "Already member",
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.REQUEST_CANCELLED: "Already cancelled",
            ActionStatus.REQUEST_DECLINED: "Already declined",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.REQUEST_DECLINED)

    async def remove_user(
        self, user_id: UUID, company_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.is_user_owner(company_id, current_user.id, self.db):
            raise UserForbidden

        action = await self.repository.get_one_or_404(
            {"user_id": user_id, "company_id": company_id}
        )
        status_to_message = {
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
            ActionStatus.INVITATION_CANCELLED: "You cancelled invitation",
            ActionStatus.INVITATION_DECLINED: "You declined invitation",
            ActionStatus.REQUEST_CANCELLED: "User cancelled request",
            ActionStatus.REQUEST_DECLINED: "User declined request",
        }

        if action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[action.status],
            )

        return await self.update_status(action, ActionStatus.REMOVED)

    async def leave_company(self, company_id: UUID, current_user: User) -> ActionDetail:
        user_action = await self.repository.get_one_or_404(
            {"user_id": current_user.id, "company_id": company_id}
        )
        status_to_message = {
            ActionStatus.OWNER: "You are owner this company",
            ActionStatus.REMOVED: "Already removed",
            ActionStatus.LEFT: "Already left",
            ActionStatus.INVITATION_CANCELLED: "You cancelled invitation",
            ActionStatus.INVITATION_DECLINED: "You declined invitation",
            ActionStatus.REQUEST_CANCELLED: "User cancelled request",
            ActionStatus.REQUEST_DECLINED: "User declined request",
        }

        if user_action.status in status_to_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=status_to_message[user_action.status],
            )

        return await self.update_status(user_action, ActionStatus.LEFT)

    async def get_users_requests_to_companies(
        self, user_id: UUID
    ) -> list[ActionDetail]:
        return await self.repository.get_requests(user_id)

    async def get_users_invitations_from_companies(
        self, user_id: UUID
    ) -> list[ActionDetail]:
        return await self.repository.get_invitations(user_id)

    # general
    async def get_users_in_company(
        self, company_id: UUID, offset: Optional[int], limit: Optional[int]
    ) -> list[UserDetail]:
        users = await self.repository.get_users_by_company(company_id, offset, limit)
        return users
