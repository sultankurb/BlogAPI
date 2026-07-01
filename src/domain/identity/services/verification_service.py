from random import randint

from fastapi import BackgroundTasks
from redis.asyncio import Redis

from src.config import settings
from src.infrastructure.notifications import AbstractNotificationInfraStructure


class VerificationService:
    def __init__(
        self, notification: AbstractNotificationInfraStructure, redis: Redis
    ) -> None:
        self._redis = redis
        self._notification = notification

    async def verification_code(
        self, email: str, background_tasks: BackgroundTasks
    ) -> None:
        code = f"{randint(0, 9999):06d}"
        await self._redis.setex(f"varification:code:{email}", 600, code)
        background_tasks.add_task(
            self._notification.send,
            to=email,
            title="Verification Code",
            text=f"Your verification code: {code} it will work in 10 minutes",
            from_who=settings.ADMIN_EMAIL,
        )
