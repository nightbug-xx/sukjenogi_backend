from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.character import Character
from app.schemas.character_homework import HomeworkCompletionUpdateRequest
from app.schemas.homework import HomeworkSelectableResponse
from app.services.character_homework_service import (
    get_homeworks_with_assignment_status,
    update_homework_completion
)

router = APIRouter(tags=["Character Homeworks"])


@router.get("/{character_id}/homeworks/selectable", response_model=list[HomeworkSelectableResponse])
def get_selectable_homeworks(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    character = db.query(Character).filter_by(id=character_id, user_id=current_user.id).first()
    if not character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")

    return get_homeworks_with_assignment_status(db, current_user.id, character_id)


@router.patch("/{character_id}/homeworks/{homework_type_id}")
def update_homework_completion_api(
    character_id: int,
    homework_type_id: int,
    body: HomeworkCompletionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_homework_completion(
        db=db,
        user_id=current_user.id,
        character_id=character_id,
        homework_type_id=homework_type_id,
        new_complete_cnt=body.complete_cnt
    )
