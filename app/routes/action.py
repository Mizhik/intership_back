from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.action import ActionDetail
from app.entity.models import User
from app.repository.action import ActionRepository
from app.services.action import ActionService
from app.services.auth import AuthService


router = APIRouter(prefix="/action", tags=["action"])


async def get_action_service(db: AsyncSession = Depends(get_db)):
    user_repository = ActionRepository(db)
    return ActionService(db, user_repository)


# C to U
@router.post("/invite/{user_id}/to/{company_id}", response_model=ActionDetail)
async def send_invitation(
    company_id: UUID,
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.send_invitation(company_id, user_id, current_user)


@router.patch(
    "/cancel-company/{invitation_id}/",
    response_model=ActionDetail,
)
async def cancel_invitation(
    invitation_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.cancel_invitation(invitation_id, current_user)


@router.patch("/accept-users/{request_id}/", response_model=ActionDetail)
async def accept_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.accept_request(request_id, current_user)


@router.patch("/decline-users/{request_id}/", response_model=ActionDetail)
async def decline_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.decline_request(request_id, current_user)


# U to C
@router.post("/request/{company_id}", response_model=ActionDetail)
async def request_to_join(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.request_to_join(company_id, current_user)


@router.patch(
    "/accept/{invitation_id}/",
    response_model=ActionDetail,
)
async def accept_invitation(
    invitation_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.accept_invitation(invitation_id, current_user)


@router.patch(
    "/decline/{invitation_id}/",
    response_model=ActionDetail,
)
async def decline_invitation(
    invitation_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.decline_invitation(invitation_id, current_user)


@router.patch("/cancel/{request_id}/", response_model=ActionDetail)
async def cancel_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.cancel_request(request_id, current_user)


# 9. Видалення користувача з компанії
@router.patch("/remove/{user_id}/of/{company_id}", response_model=ActionDetail)
async def remove_user(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.remove_user(user_id, company_id, current_user)


# 10. Вихід користувача з компанії
@router.patch("/leave/{company_id}", response_model=ActionDetail)
async def leave_company(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.leave_company(company_id, current_user)


@router.patch("/append-admin/{user_id}/in/{company_id}", response_model=ActionDetail)
async def create_admin(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.create_admin(company_id, user_id, current_user)


@router.patch("/remove-admin/{user_id}/from/{company_id}", response_model=ActionDetail)
async def remove_admin(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.remove_admin(company_id, user_id, current_user)
