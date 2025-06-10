from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class FriendRequestStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    cancelled = "cancelled"


class FriendRequestCreate(BaseModel):
    to_user_email: str


class FriendRequestResponse(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    from_user_email: str | None = None
    to_user_email: str | None = None
    status: FriendRequestStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FriendResponse(BaseModel):
    id: int
    user_id_1: int
    user_id_2: int
    created_at: datetime

    class Config:
        orm_mode = True
