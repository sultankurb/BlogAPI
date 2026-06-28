from email.message import EmailMessage

import aiosmtplib

from src.config import settings
from src.infrastructure.notifications.abstract import (
    AbstractNotificationInfraStructure,
)


class MailpitNotificationService(AbstractNotificationInfraStructure):
    @classmethod
    async def send(
            cls,
            to: str,
            title: str,
            text: str,
            from_who: str
    ) -> None:
        message = EmailMessage()
        message["Subject"] = title
        message["T0"] = to
        message["From"] = from_who
        message.set_content(text)
        await aiosmtplib.send(message, hostname="", port=00)
