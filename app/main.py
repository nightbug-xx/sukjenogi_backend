#pp/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import traceback

from app.api import user, auth, character, homework, character_homework, dashboard

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

app = FastAPI(
    title="숙제노기 API",
    description="마비노기 모바일 숙제 관리용 백엔드 API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
    root_path="/api"
)

@app.middleware("http")
async def log_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        print("❌ 전역 예외 발생:")
        traceback.print_exc()
        raise

origins = [
    "https://sukjenogi.biryu2000.kr",  # 프론트 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(character.router, prefix="/characters", tags=["Characters"])
app.include_router(homework.router, prefix="/homeworks", tags=["Homeworks"])
app.include_router(character_homework.router, prefix="/characterHomework", tags=["Character Homeworks"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def read_root():
        return {"message": "숙제노기 서버가 잘 작동 중입니다."}

