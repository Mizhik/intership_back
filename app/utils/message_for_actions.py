from fastapi import HTTPException, status
from app.entity.enums import ActionStatus


async def send_invitation_status_msg(action):
    status_to_message = {
        ActionStatus.REQUESTED_TO_JOIN: "This user already request to your company",
        ActionStatus.INVITED: "You already invited this user",
        ActionStatus.MEMBER: "This user already member your company",
        ActionStatus.OWNER: "You can invite this user, cause he owner this company",
        ActionStatus.ADMIN: "You can invite this user, cause he admin this company",
        ActionStatus.INVITATION_CANCELLED: "You can`t send invite, cause user cancelled invitation",
        ActionStatus.INVITATION_DECLINED: "You can`t send invite, cause user declined invitation",
        ActionStatus.REMOVED: "You removed this user",
        ActionStatus.LEFT: "User leave this company",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )


async def cancel_invitation_status_msg(action):
    status_to_message = {
        ActionStatus.MEMBER: "This user already member your company",
        ActionStatus.OWNER: "You can cancel this user, cause he owner this company",
        ActionStatus.ADMIN: "You can cancel this user, cause he admin this company",
        ActionStatus.INVITATION_CANCELLED: "You can`t cancel invite, cause user cancelled invitation",
        ActionStatus.INVITATION_DECLINED: "You can`t cancel invite, cause user declined invitation",
        ActionStatus.REMOVED: "You removed this user",
        ActionStatus.LEFT: "User leave this company",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )


async def accept_invitation_status_msg(action):
    status_to_message = {
        ActionStatus.INVITED: "You must wait for the user to respond",
        ActionStatus.MEMBER: "This user already member your company",
        ActionStatus.OWNER: "You can accept this user, cause he owner this company",
        ActionStatus.ADMIN: "You can accept this user, cause he admin this company",
        ActionStatus.INVITATION_CANCELLED: "You can`t  accept invite, cause user cancelled invitation",
        ActionStatus.INVITATION_DECLINED: "You can`t accept invite, cause user declined invitation",
        ActionStatus.REMOVED: "You removed this user",
        ActionStatus.LEFT: "User leave this company",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )


async def decline_invitation_status_msg(action):
    status_to_message = {
        ActionStatus.INVITED: "You must wait for the user to respond",
        ActionStatus.MEMBER: "This user already member your company",
        ActionStatus.OWNER: "You can decline this user, cause he owner this company",
        ActionStatus.ADMIN: "You can decline this user, cause he admin this company",
        ActionStatus.INVITATION_CANCELLED: "You can`t  declined invite, cause user cancelled invitation",
        ActionStatus.INVITATION_DECLINED: "You can`t declined invite, cause user declined invitation",
        ActionStatus.REMOVED: "You removed this user",
        ActionStatus.LEFT: "User leave this company",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )


async def request_to_join_status_msg(action):
    status_to_message = {
        ActionStatus.REQUESTED_TO_JOIN: "You can't requested to join, because you already send request",
        ActionStatus.MEMBER: "Yo can't send request, cause you already member",
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
        ActionStatus.INVITED: "Already invited",
        ActionStatus.REQUEST_CANCELLED: "You can't send request, you cancelled request",
        ActionStatus.REQUEST_DECLINED: "You can't send request, you declined request",
        ActionStatus.REMOVED: "You've been removed from this company",
        ActionStatus.LEFT: "You leave from this company",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )


async def cancel_request_status_msg(action):
    status_to_message = {
        ActionStatus.MEMBER: "Already member",
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
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


async def accept_request_status_msg(action):
    status_to_message = {
        ActionStatus.MEMBER: "Already member",
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
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


async def decline_request_status_msg(action):
    status_to_message = {
        ActionStatus.MEMBER: "Already member",
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
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


async def remove_user_status_msg(action):
    status_to_message = {
        ActionStatus.MEMBER: "Already member",
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
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


async def leave_company_status_msg(action):
    status_to_message = {
        ActionStatus.MEMBER: "Already member",
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
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

async def create_admin_status_msg(action):
    status_to_message = {
        ActionStatus.OWNER: "You are owner this company",
        ActionStatus.ADMIN: "You are admin this company",
        ActionStatus.REMOVED: "Already removed",
        ActionStatus.LEFT: "Already left",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )

async def remove_admin_status_msg(action):
    status_to_message = {
        ActionStatus.OWNER: "This user is owner this company",
        ActionStatus.REMOVED: "Already removed",
        ActionStatus.LEFT: "Already left",
    }

    if action.status in status_to_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=status_to_message[action.status],
        )
