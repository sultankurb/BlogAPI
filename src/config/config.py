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
    ADMIN_USERNAME: str = ""
    ADMIN_PASSWORD: str = ""
    ADMIN_EMAIL: str = ""
    environment: str = "development"
    EMAIL_HOST: str = "0.0.0.0"
    EMAIL_PORT: int = 1025
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
        "http://127.0.0.1:8000",
    ]

def get_app_config() -> AppConfig:
    return AppConfig()


settings = get_app_config()
