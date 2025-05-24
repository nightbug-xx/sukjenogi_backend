from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services.dashboard_service import (
    get_dashboard_characters,
    get_dashboard_homeworks_for_character
)

router = APIRouter(tags=["Dashboard"])

@router.get("/characters")
def dashboard_characters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_characters(db, current_user.id)


@router.get("/characters/{character_id}/homeworks")
def dashboard_homeworks(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_homeworks_for_character(db, current_user.id, character_id)
