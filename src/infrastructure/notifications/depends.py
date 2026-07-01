from src.config import settings
from src.infrastructure.notifications.abstract import (
    AbstractNotificationInfraStructure,
)
from src.infrastructure.notifications.local import MailpitNotificationService
from src.infrastructure.notifications.production import (
    ProductionNotificationInfraStructure,
)

_notification_service: AbstractNotificationInfraStructure | None = None

def get_notification_service() -> AbstractNotificationInfraStructure:
    global _notification_service
    if _notification_service is None:
        if settings.environment == "development":
            _notification_service = MailpitNotificationService()
        else:
            _notification_service = ProductionNotificationInfraStructure()
    return _notification_service