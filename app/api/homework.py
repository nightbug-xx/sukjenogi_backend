from datetime import datetime, time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.homework import HomeworkType
from app.models.user import User
from app.schemas.homework import HomeworkTypeCreate, HomeworkTypeResponse
from app.crud.homework import create_homework_type, get_homework_types_by_user

router = APIRouter()

@router.post("", response_model=HomeworkTypeResponse)
def register_homework_type(
    homework_data: HomeworkTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    homework_type = HomeworkType(
        user_id=current_user.id,
        title=homework_data.title,
        description=homework_data.description,
        reset_type=homework_data.reset_type,
        reset_time=homework_data.reset_time or time(6, 0),
        clear_count=homework_data.clear_count or 0,
        created_at=datetime.utcnow(),
    )
    db.add(homework_type)
    db.commit()
    db.refresh(homework_type)
    return homework_type

@router.get("", response_model=List[HomeworkTypeResponse])
def list_homework_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_homework_types_by_user(current_user.id, db)
