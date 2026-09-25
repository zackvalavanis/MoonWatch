from pydantic import ConfigDict
from pydantic_settings import BaseSettings

CORS_ORIGINS = [
    "https://localhost:5173",
    "https://localhost:5174",
    "https://localhost:5175",
]


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()
