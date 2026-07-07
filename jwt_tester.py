from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jwt

private_key = Path(__file__).parent / 'certificates' / 'private-key.pem'

def encode_token(payload: dict[str, Any]) -> str:
    to_encode = payload.copy()
    now = datetime.now(tz=timezone.utc)
    expire = now + timedelta(minutes=30)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key.read_text(),
        algorithm="RS256",
    )
    return encoded


print(encode_token(payload={"sub": "14000", "roles": ["admin", "user"]}))
