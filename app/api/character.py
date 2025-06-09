from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdateRequest, CharacterDetailResponse, CharacterOrderUpdate
from app.schemas.homework import HomeworkSelectableResponse
from app.crud.character import create_character, get_characters_by_user
from app.services.character_homework_service import get_homeworks_with_assignment_status, assign_homework_to_character, unassign_homework_from_character
from app.models.user import User
from app.models.character import Character
from app.core.deps import get_db, get_current_user

router = APIRouter()


@router.post("", response_model=CharacterResponse)
def register_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_character(current_user.id, character_data, db)


@router.get("", response_model=List[CharacterResponse])
def list_my_characters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_characters_by_user(current_user.id, db)


@router.get("/{character_id}/homeworks/selectable", response_model=List[HomeworkSelectableResponse])
def get_selectable_homeworks(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    character = db.query(Character).filter_by(id=character_id, user_id=current_user.id).first()
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")

    return get_homeworks_with_assignment_status(db, current_user.id, character_id)

@router.post("/{character_id}/homeworks/{homework_type_id}")
def assign_homework(
    character_id: int,
    homework_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return assign_homework_to_character(db, current_user.id, character_id, homework_type_id)


@router.delete("/{character_id}/homeworks/{homework_type_id}")
def unassign_homework(
    character_id: int,
    homework_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return unassign_homework_from_character(db, current_user.id, character_id, homework_type_id)

@router.put("/{character_id}")
def update_character(
    character_id: int,
    req: CharacterUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    character = db.query(Character).filter(Character.id == character_id).first()

    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    character.name = req.name
    character.server = req.server
    character.combat_power = req.power
    db.commit()
    return {"message": "캐릭터가 수정되었습니다."}

@router.delete("/{character_id}")
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    character = db.query(Character).filter(Character.id == character_id).first()

    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    db.delete(character)
    db.commit()
    return {"message": "캐릭터가 삭제되었습니다."}

@router.get("/{character_id}", response_model=CharacterDetailResponse)
def get_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user = db.merge(current_user)

    character = db.query(Character).filter(Character.id == character_id).first()

    if not character or character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    return character

@router.patch("/order")
def update_character_order(
    updates: List[CharacterOrderUpdate],
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    for update in updates:
        character = db.query(Character).filter_by(id=update.id, user_id=user.id).first()
        if character:
            character.order = update.order
            character.order = update.order
            db.add(character)
    db.commit()
    return {"status": "ok"}