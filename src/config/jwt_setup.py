from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel


class JWTConfig(BaseModel):
    public_key: Path
    private_key: Path
    algorithm: str = "RS256"
    token_expire_minutes: timedelta = timedelta(minutes=30)
    refresh_expire_days: timedelta = timedelta(days=30)
