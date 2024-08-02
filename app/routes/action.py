from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.dtos.action import ActionDetail
from app.dtos.user import UserDetail
from app.entity.models import User
from app.repository.action import ActionRepository
from app.services.action import ActionService
from app.services.auth import AuthService


router = APIRouter(prefix="/action", tags=["action"])


async def get_action_service(db: AsyncSession = Depends(get_db)):
    user_repository = ActionRepository(db)
    return ActionService(db, user_repository)


# 1. Відправка запрошень
@router.post(
    "/companies/{company_id}/invitations-to/{user_id}", response_model=ActionDetail
)
async def send_invitation(
    company_id: UUID,
    user_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.send_invitation(company_id, user_id, current_user)


# 2. Скасування запрошення
@router.patch(
    "/companies/{company_id}/invitations/{invitation_id}/cancel",
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
    "/invitations/{company_id}/invitations{invitation_id}/accept",
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
    "/invitations/{company_id}/invitations{invitation_id}/decline",
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
@router.post("/companies/{company_id}/requests", response_model=ActionDetail)
async def request_to_join(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.request_to_join(company_id, current_user)


# 6. Скасування запиту на приєднання
@router.patch("/requests/{request_id}/cancel", response_model=ActionDetail)
async def cancel_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.cancel_request(request_id, current_user)


# 7. Прийняття запиту на приєднання
@router.patch("/requests/{request_id}/accept", response_model=ActionDetail)
async def accept_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.accept_request(request_id, current_user)


# 8. Відхилення запиту на приєднання
@router.patch("/requests/{request_id}/decline", response_model=ActionDetail)
async def decline_request(
    request_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.decline_request(request_id, current_user)


# 9. Видалення користувача з компанії
@router.patch("/companies/{company_id}/user/{user_id}", response_model=ActionDetail)
async def remove_user(
    user_id: UUID,
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.remove_user(user_id, company_id, current_user)


# 10. Вихід користувача з компанії
@router.patch("/companies/{company_id}/leave", response_model=ActionDetail)
async def leave_company(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.leave_company(company_id, current_user)


# 13. Перегляд списку запрошених користувачів власником
@router.get("/companies/{company_id}/invitations", response_model=list[ActionDetail])
async def view_company_invitations(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.get_company_invitations_to_users(
        company_id, current_user
    )


# 14. Перегляд списку запитів на приєднання власником
@router.get("/companies/{company_id}/requests", response_model=list[ActionDetail])
async def view_requests(
    company_id: UUID,
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.get_company_requests_to_users(company_id, current_user)


# 11. Перегляд запитів на приєднання користувачем
@router.get("/requests", response_model=list[ActionDetail])
async def view_user_requests(
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.get_users_requests_to_companies(current_user.id)


# 12. Перегляд запрошень користувачем
@router.get("/invitations", response_model=list[ActionDetail])
async def view_user_invitations(
    current_user: User = Depends(AuthService.get_current_user),
    action_service=Depends(get_action_service),
):
    return await action_service.get_users_invitations_from_companies(current_user.id)


# 15. Перегляд списку користувачів компанії з пагінацією
@router.get("/companies/{company_id}/members", response_model=list[UserDetail])
async def view_users_in_company(
    company_id: UUID,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    action_service=Depends(get_action_service),
):
    return await action_service.get_users_in_company(company_id, offset, limit)
