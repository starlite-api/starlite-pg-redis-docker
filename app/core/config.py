import os
import secrets

from databases import DatabaseURL
from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    API_V1_STR: str = "/api/v1"
    FILE_STORAGE_ROUTE: str = os.path.abspath("app") + "/files/"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day in minutes
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    # Database Connection
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: DatabaseURL

    @validator("DATABASE_URL", pre=True)
    def set_database_url(cls, v: str | None) -> DatabaseURL:
        if not v:
            raise ValueError("Missing DATABASE_URL")
        if "postgresql" not in v and "postgres" in v:
            # Heroku supplies DATABASE_URL with the wrong driver for SQLAlchemy
            v = v.replace("postgres", "postgresql")
        if "asyncpg" not in v:
            v = v.replace("postgresql", "postgresql+asyncpg")
        return DatabaseURL(v)

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False
    TESTING: bool = False
    REDIS_URL: str


settings = Settings()
