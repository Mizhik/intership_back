from enum import Enum


class ActionStatus(Enum):
    INVITED = "invited"
    INVITATION_CANCELLED = "invitation_cancelled"
    INVITATION_DECLINED = "invitation_declined"

    REQUESTED_TO_JOIN = "requested_to_join"
    REQUEST_CANCELLED = "request_cancelled"
    REQUEST_DECLINED = "request_declined"
    
    REMOVED = "removed"
    LEFT = "left"
    
    MEMBER = "member"
    OWNER = "owner"
    ADMIN = "admin"
