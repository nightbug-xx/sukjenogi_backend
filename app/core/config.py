# app/core/config.py

from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()

# 베이스 클래스
Base = declarative_base()

