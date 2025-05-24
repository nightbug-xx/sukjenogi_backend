from pydantic import BaseModel

class DashboardCharacter(BaseModel):
    character_id: int
    character_name: str
    server: str
    
class DashboardHomework(BaseModel):
    homework_id: int
    title: str
    reset_type: str
    clear_count: int
    complete_cnt: int