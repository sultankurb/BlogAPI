from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
    )
    DATABASE_URL: str | None = None
    REDIS_URL: str | None = None


def get_app_config() -> AppConfig:
    return AppConfig()


settings = get_app_config()
