from sqlalchemy.orm import Session
from app.models.friend import FriendRequest, Friend, FriendRequestStatus
from app.models.user import User
from app.models.character import Character, CharacterHomework
from app.models.homework import HomeworkType
from fastapi import HTTPException, status
from datetime import datetime


def send_friend_request(db: Session, from_user_id: int, to_user_email: str):
    to_user = db.query(User).filter(User.email == to_user_email).first()
    if not to_user:
        raise HTTPException(status_code=404, detail="해당 이메일의 유저를 찾을 수 없습니다.")

    if to_user.id == from_user_id:
        raise HTTPException(status_code=400, detail="자기 자신에게 친구 요청을 보낼 수 없습니다.")

    # 이미 친구인지 확인
    user_ids = sorted([from_user_id, to_user.id])
    existing_friend = db.query(Friend).filter(
        Friend.user_id_1 == user_ids[0],
        Friend.user_id_2 == user_ids[1]
    ).first()
    if existing_friend:
        raise HTTPException(status_code=400, detail="이미 친구 상태입니다.")

    # 이미 pending 요청이 있는지 확인
    existing_request = db.query(FriendRequest).filter(
        FriendRequest.from_user_id == from_user_id,
        FriendRequest.to_user_id == to_user.id,
        FriendRequest.status == FriendRequestStatus.pending
    ).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="이미 친구 요청을 보낸 상태입니다.")

    friend_request = FriendRequest(
        from_user_id=from_user_id,
        to_user_id=to_user.id,
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return friend_request


def get_received_requests(db: Session, user_id: int):
    return db.query(FriendRequest).filter(
        FriendRequest.to_user_id == user_id,
        FriendRequest.status == FriendRequestStatus.pending
    ).all()


def get_sent_requests(db: Session, user_id: int):
    return db.query(FriendRequest).filter(
        FriendRequest.from_user_id == user_id,
        FriendRequest.status == FriendRequestStatus.pending
    ).all()


def cancel_sent_request(db: Session, request_id: int, user_id: int):
    request = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.from_user_id == user_id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="요청을 찾을 수 없습니다.")

    request.status = FriendRequestStatus.cancelled
    request.updated_at = datetime.utcnow()
    db.commit()


def respond_to_request(db: Session, request_id: int, user_id: int, accept: bool):
    request = db.query(FriendRequest).filter(
        FriendRequest.id == request_id,
        FriendRequest.to_user_id == user_id,
        FriendRequest.status == FriendRequestStatus.pending
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="요청을 찾을 수 없습니다.")

    request.status = FriendRequestStatus.accepted if accept else FriendRequestStatus.rejected
    request.updated_at = datetime.utcnow()

    # 친구 수락 시 friends 테이블에도 저장
    if accept:
        user_ids = sorted([request.from_user_id, request.to_user_id])
        friend = Friend(
            user_id_1=user_ids[0],
            user_id_2=user_ids[1]
        )
        db.add(friend)

    db.commit()


def get_friend_list(db: Session, user_id: int):
    friends = db.query(Friend).filter(
        (Friend.user_id_1 == user_id) | (Friend.user_id_2 == user_id)
    ).all()

    result = []
    for f in friends:
        friend_id = f.user_id_2 if f.user_id_1 == user_id else f.user_id_1
        result.append(friend_id)

    return result

def get_public_characters_of_friend(db: Session, current_user_id: int, friend_id: int):
    # 친구 관계 확인
    user_ids = sorted([current_user_id, friend_id])
    is_friend = db.query(Friend).filter(
        Friend.user_id_1 == user_ids[0],
        Friend.user_id_2 == user_ids[1]
    ).first()

    if not is_friend:
        raise HTTPException(status_code=403, detail="친구가 아닙니다.")

    # 공개된 캐릭터 목록
    characters = db.query(Character).filter(
        Character.user_id == friend_id,
        Character.is_public == True
    ).all()

    return characters

def get_public_homeworks_of_friend_character(
    db: Session,
    current_user_id: int,
    friend_id: int,
    character_id: int
):
    # 1. 친구인지 확인
    user_ids = sorted([current_user_id, friend_id])
    is_friend = db.query(Friend).filter(
        Friend.user_id_1 == user_ids[0],
        Friend.user_id_2 == user_ids[1]
    ).first()
    if not is_friend:
        raise HTTPException(status_code=403, detail="친구가 아닙니다.")

    # 2. 해당 캐릭터가 공개인지 확인
    character = db.query(Character).filter(
        Character.id == character_id,
        Character.user_id == friend_id,
        Character.is_public == True
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="공개된 캐릭터를 찾을 수 없습니다.")

    # 3. 공개된 숙제만 조회
    results = db.query(HomeworkType).join(CharacterHomework).filter(
        CharacterHomework.character_id == character_id,
        HomeworkType.is_public == True
    ).all()

    return results

def delete_friend(db: Session, user_id: int, friend_id: int):
    user_ids = sorted([user_id, friend_id])

    friend = db.query(Friend).filter(
        Friend.user_id_1 == user_ids[0],
        Friend.user_id_2 == user_ids[1]
    ).first()

    if not friend:
        raise HTTPException(status_code=404, detail="친구 관계가 존재하지 않습니다.")

    db.delete(friend)
    db.commit()
