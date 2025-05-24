from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.character import CharacterCreate, CharacterResponse
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
