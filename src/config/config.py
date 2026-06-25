from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config.jwt_setup import JWTConfig

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PRIVATE_KEY_PATH = BASE_DIR / 'certificates' / 'private-key.pem'
PUBLIC_KEY_PATH = BASE_DIR / 'certificates' / 'public-key.pem'


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
    )
    DATABASE_URL: str | None = None
    REDIS_URL: str | None = None
    DEFAULT_USERS_ROLES: list[str] = ["user", "admin", "moderator"]
    jwt: JWTConfig = JWTConfig(
        private_key=PRIVATE_KEY_PATH,
        public_key=PUBLIC_KEY_PATH,
    )


def get_app_config() -> AppConfig:
    return AppConfig()


settings = get_app_config()
