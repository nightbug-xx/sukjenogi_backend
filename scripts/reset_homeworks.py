import datetime
from dotenv import load_dotenv  # 👈 추가
load_dotenv()  # 👈 반드시 최상단에서 실행

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.character import CharacterHomework
from app.models.homework import HomeworkType

def reset_homeworks():
    db: Session = SessionLocal()
    now = datetime.datetime.now()
    weekday = now.weekday()  # 0: 월요일
    day = now.day  # 1: 매월 1일

    reset_targets = ["daily"]
    if weekday == 0:
        reset_targets.append("weekly")
    if day == 1:
        reset_targets.append("monthly")

    # 초기화 대상 조회
    character_homeworks = (
        db.query(CharacterHomework)
        .join(HomeworkType, CharacterHomework.homework_type_id == HomeworkType.id)
        .filter(HomeworkType.reset_type.in_(reset_targets))
        .all()
    )

    for ch in character_homeworks:
        ch.is_done = False
        ch.complete_cnt = 0

    db.commit()
    db.close()
    print(f"[{now}] 초기화 완료: {len(character_homeworks)}건 처리됨")

if __name__ == "__main__":
    reset_homeworks()
