# app/schemas/character_homework.py

from pydantic import BaseModel

class HomeworkCompletionUpdateRequest(BaseModel):
    complete_cnt: int
