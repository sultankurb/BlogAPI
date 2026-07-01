from email.message import EmailMessage

import aiosmtplib

from src.config import settings
from src.infrastructure.notifications.abstract import (
    AbstractNotificationInfraStructure,
)


class MailpitNotificationService(AbstractNotificationInfraStructure):
    async def send(
            self,
            to: str,
            title: str,
            text: str,
            from_who: str
    ) -> None:
        message = EmailMessage()
        message["Subject"] = title
        message["To"] = to
        message["From"] = from_who
        message.set_content(text)
        await aiosmtplib.send(
            message,
            hostname=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT
        )
