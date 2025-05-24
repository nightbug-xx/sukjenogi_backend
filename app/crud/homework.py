from sqlalchemy.orm import Session
from app.models.homework import HomeworkType
from app.schemas.homework import HomeworkTypeCreate

def create_homework_type(user_id: int, data: HomeworkTypeCreate, db: Session):
    new_homework = HomeworkType(
        user_id=user_id,
        name=data.name,
        reset_time=data.reset_time,
        clear_count=data.clear_count,
    )
    db.add(new_homework)
    db.commit()
    db.refresh(new_homework)
    return new_homework

def get_homework_types_by_user(user_id: int, db: Session):
    return db.query(HomeworkType).filter(HomeworkType.user_id == user_id).all()
