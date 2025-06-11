from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.friend import (
    FriendRequestCreate,
    FriendRequestResponse,
    FriendResponse,
    FriendListItem,
)
from app.schemas.character import CharacterResponse
from app.services import friend_service
from app.models.user import User

router = APIRouter()


@router.post("/request", response_model=FriendRequestResponse)
def send_request(
    request_data: FriendRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return friend_service.send_friend_request(db, current_user.id, request_data.to_user_email)


@router.get("/requests/received", response_model=list[FriendRequestResponse])
def get_received_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return friend_service.get_received_requests(db, current_user.id)


@router.get("/requests/sent", response_model=list[FriendRequestResponse])
def get_sent_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return friend_service.get_sent_requests(db, current_user.id)


@router.post("/requests/{request_id}/cancel")
def cancel_sent_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friend_service.cancel_sent_request(db, request_id, current_user.id)
    return {"detail": "요청을 취소했습니다."}


@router.post("/requests/{request_id}/respond")
def respond_to_request(
    request_id: int,
    accept: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friend_service.respond_to_request(db, request_id, current_user.id, accept)
    return {"detail": "요청을 처리했습니다."}


@router.get("/list", response_model=list[FriendListItem])
def get_friend_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return friend_service.get_friend_list(db, current_user.id)

@router.get("/{friend_id}/characters", response_model=list[CharacterResponse])
def get_friend_characters(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return friend_service.get_public_characters_of_friend(db, current_user.id, friend_id)

@router.delete("/{friend_id}")
def delete_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friend_service.delete_friend(db, current_user.id, friend_id)
    return {"detail": "친구가 삭제되었습니다."}
