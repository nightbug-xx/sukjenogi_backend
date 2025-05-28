from datetime import datetime, time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.homework import HomeworkType
from app.models.user import User
from app.schemas.homework import HomeworkTypeCreate, HomeworkTypeResponse, HomeworkTypeUpdateRequest, HomeworkTypeDetailResponse, HomeworkTypeOrderUpdate
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

@router.put("/{homework_type_id}")
def update_homework_type(
    homework_type_id: int,
    req: HomeworkTypeUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user = db.merge(current_user)

    homework_type = db.query(HomeworkType).filter(HomeworkType.id == homework_type_id).first()

    if not homework_type or homework_type.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    homework_type.name = req.name
    homework_type.description = req.description
    homework_type.repeat_type = req.repeat_type
    homework_type.repeat_count = req.repeat_count

    db.commit()
    return {"message": "숙제가 수정되었습니다."}

@router.delete("/{homework_type_id}")
def delete_homework_type(
    homework_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user = db.merge(current_user)

    homework_type = db.query(HomeworkType).filter(HomeworkType.id == homework_type_id).first()

    if not homework_type or homework_type.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    db.delete(homework_type)
    db.commit()
    return {"message": "숙제가 삭제되었습니다."}

@router.get("/{homework_type_id}", response_model=HomeworkTypeDetailResponse)
def get_homework_type(
    homework_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user = db.merge(current_user)

    homework_type = db.query(HomeworkType).filter(HomeworkType.id == homework_type_id).first()

    if not homework_type or homework_type.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    return homework_type

@router.patch("/order")
def update_homework_type_order(
    updates: List[HomeworkTypeOrderUpdate],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    for update in updates:
        hw_type = db.query(HomeworkType).filter_by(id=update.id, user_id=user.id).first()
        if hw_type and hw_type.order != update.order:
            hw_type.order = update.order
            db.add(hw_type)
    db.commit()
    return {"status": "ok"}
