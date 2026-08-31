from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml/models/model_v1.joblib")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "replace-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

settings = Settings()
