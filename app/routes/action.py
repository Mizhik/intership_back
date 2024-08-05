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


# 1. Відправка запрошень
@router.post("/invite/{user_id}/to/{company_id}", response_model=ActionDetail)
async def send_invitation(
    company_id: UUID,
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.send_invitation(company_id, user_id, current_user)


# 2. Скасування запрошення
@router.patch(
    "/cancel/{invitation_id}/for/{company_id}",
    response_model=ActionDetail,
)
async def cancel_invitation(
    company_id: UUID,
    invitation_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.cancel_invitation(
        company_id, invitation_id, current_user
    )


# 3. Прийняття запрошення
@router.patch(
    "/accept/{invitation_id}/for{company_id}",
    response_model=ActionDetail,
)
async def accept_invitation(
    company_id: UUID,
    invitation_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.accept_invitation(
        company_id, invitation_id, current_user
    )


# 4. Відхилення запрошення
@router.patch(
    "/decline/{invitation_id}/for{company_id}",
    response_model=ActionDetail,
)
async def decline_invitation(
    company_id: UUID,
    invitation_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.decline_invitation(
        company_id, invitation_id, current_user
    )


# 5. Запит на приєднання до компанії
@router.post("/request/{company_id}", response_model=ActionDetail)
async def request_to_join(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.request_to_join(company_id, current_user)


# 6. Скасування запиту на приєднання
@router.patch("/cancel/{request_id}/", response_model=ActionDetail)
async def cancel_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.cancel_request(request_id, current_user)


# 7. Прийняття запиту на приєднання
@router.patch("/accept/{request_id}/", response_model=ActionDetail)
async def accept_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.accept_request(request_id, current_user)


# 8. Відхилення запиту на приєднання
@router.patch("/decline/{request_id}/", response_model=ActionDetail)
async def decline_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.decline_request(request_id, current_user)


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
