from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.friend import Friend, FriendRequest, FriendRequestStatus
from app.models.character import Character

def get_user_public_info(
    db: Session,
    current_user_id: int,
    target_email: str
):
    target_user = db.query(User).filter(User.email == target_email).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="해당 유저를 찾을 수 없습니다.")

    if target_user.id == current_user_id:
        raise HTTPException(status_code=400, detail="자기 자신은 검색할 수 없습니다.")

    user_ids = sorted([current_user_id, target_user.id])
    is_friend = db.query(Friend).filter(
        Friend.user_id_1 == user_ids[0],
        Friend.user_id_2 == user_ids[1]
    ).first() is not None

    request_sent = db.query(FriendRequest).filter(
        FriendRequest.from_user_id == current_user_id,
        FriendRequest.to_user_id == target_user.id,
        FriendRequest.status == FriendRequestStatus.pending
    ).first() is not None

    request_received = db.query(FriendRequest).filter(
        FriendRequest.from_user_id == target_user.id,
        FriendRequest.to_user_id == current_user_id,
        FriendRequest.status == FriendRequestStatus.pending
    ).first() is not None

    return {
        "id": target_user.id,
        "email": target_user.email,
        "is_friend": is_friend,
        "request_sent": request_sent,
        "request_received": request_received,
    }

def get_user_by_character(
    db: Session,
    server: str,
    name: str
):
    character = db.query(Character).filter(
        Character.server == server,
        Character.name == name
    ).first()

    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")

    user = db.query(User).filter(User.id == character.user_id).first()

    return {
        "user_id": user.id,
        "email": user.email,
        "character_id": character.id,
        "character_name": character.name,
        "server": character.server,
        "is_public": character.is_public
    }