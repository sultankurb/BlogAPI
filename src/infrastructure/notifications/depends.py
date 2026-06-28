from src.config import settings
from src.infrastructure.notifications import (
    AbstractNotificationInfraStructure,
    MailpitNotificationService,
    ProductionNotificationInfraStructure,
)

# Ленивая инициализация, чтобы не плодить объекты
_notification_service: AbstractNotificationInfraStructure | None = None

def get_notification_service() -> AbstractNotificationInfraStructure:
    global _notification_service
    if _notification_service is None:
        if settings.environment == "development":
            _notification_service = MailpitNotificationService()
        else:
            _notification_service = ProductionNotificationInfraStructure()
    return _notification_service