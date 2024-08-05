from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.action import ActionDetail
from app.entity.enums import ActionStatus
from app.entity.models import User
from app.repository.action import ActionRepository
from app.services.errors import UserForbidden
from app.utils.message_for_actions import (
    accept_invitation_status_msg,
    accept_request_status_msg,
    cancel_invitation_status_msg,
    cancel_request_status_msg,
    create_admin_status_msg,
    decline_invitation_status_msg,
    decline_request_status_msg,
    leave_company_status_msg,
    remove_admin_status_msg,
    remove_user_status_msg,
    request_to_join_status_msg,
    send_invitation_status_msg,
)


class ActionService:

    def __init__(self, db: AsyncSession, repository: ActionRepository):
        self.db = db
        self.repository = repository

    # C to U
    async def send_invitation(
        self, company_id: UUID, user_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden

        user_action = await self.repository.get_one(
            user_id=user_id, company_id=company_id
        )

        await send_invitation_status_msg(user_action)

        if not user_action:
            action = dict(
                user_id=user_id, company_id=company_id, status=ActionStatus.INVITED
            )
            return await self.repository.create(action)

    async def cancel_invitation(
        self, invitation_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404({"id": invitation_id})

        if not await self.repository.is_user_owner_or_admin(
            action.company_id, current_user.id
        ):
            raise UserForbidden

        await cancel_invitation_status_msg(action)
        return await self.repository.update(
            action.id, {"status": ActionStatus.INVITATION_CANCELLED}
        )

    async def accept_request(
        self, request_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404({"id": request_id})

        if not await self.repository.is_user_owner_or_admin(
            action.company_id, current_user.id
        ):
            raise UserForbidden

        await accept_invitation_status_msg(action)
        return await self.repository.update(action.id, {"status": ActionStatus.MEMBER})

    async def decline_request(
        self, invitation_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404({"id": invitation_id})

        if not await self.repository.is_user_owner_or_admin(
            action.company_id, current_user.id
        ):
            raise UserForbidden

        await decline_invitation_status_msg(action)

        return await self.repository.update(
            action.id, {"status": ActionStatus.REQUEST_DECLINED}
        )

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

        await request_to_join_status_msg(action)

    async def cancel_request(
        self, request_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404(
            {"id": request_id, "user_id": current_user.id}
        )

        await cancel_request_status_msg(action)

        return await self.repository.update(
            action.id, {"status": ActionStatus.REQUEST_CANCELLED}
        )

    async def accept_invitation(
        self, invitation_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404(
            {"id": invitation_id, "user_id": current_user.id}
        )
        await accept_request_status_msg(action)

        return await self.repository.update(action.id, {"status": ActionStatus.MEMBER})

    async def decline_invitation(
        self, request_id: UUID, current_user: User
    ) -> ActionDetail:
        action = await self.repository.get_one_or_404(
            {"id": request_id, "user_id": current_user.id}
        )

        await decline_request_status_msg(action)

        return await self.repository.update(
            action.id, {"status": ActionStatus.INVITATION_DECLINED}
        )

    async def remove_user(
        self, user_id: UUID, company_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden

        action = await self.repository.get_one_or_404(
            {"user_id": user_id, "company_id": company_id}
        )
        await remove_user_status_msg(action)
        return await self.repository.update(action.id, {"status": ActionStatus.REMOVED})

    async def leave_company(self, company_id: UUID, current_user: User) -> ActionDetail:
        user_action = await self.repository.get_one_or_404(
            {"user_id": current_user.id, "company_id": company_id}
        )
        await leave_company_status_msg(user_action)
        return await self.repository.update(
            user_action.id, {"status": ActionStatus.LEFT}
        )

    async def create_admin(
        self, company_id: UUID, user_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden
        user_action = await self.repository.get_one(
            user_id=user_id, company_id=company_id
        )
        await create_admin_status_msg(user_action)
        return await self.repository.update(
            user_action.id, {"status": ActionStatus.ADMIN}
        )

    async def remove_admin(
        self, company_id: UUID, user_id: UUID, current_user: User
    ) -> ActionDetail:
        if not await self.repository.is_user_owner_or_admin(
            company_id, current_user.id
        ):
            raise UserForbidden
        user_action = await self.repository.get_one(
            user_id=user_id, company_id=company_id
        )
        await remove_admin_status_msg(user_action)
        return await self.repository.update(
            user_action.id, {"status": ActionStatus.MEMBER}
        )
