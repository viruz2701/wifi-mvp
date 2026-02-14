from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    SECRET_KEY: str
    ENCRYPTION_KEY: str  # for Fernet
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    BACKEND_PORT: int = 8000

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()