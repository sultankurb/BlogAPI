__all__ = [
    'AbstractNotificationInfraStructure',
    'MailpitNotificationService',
    'ProductionNotificationInfraStructure',
    'get_notification_service',
]

from src.infrastructure.notifications.abstract import (
    AbstractNotificationInfraStructure,
)
from src.infrastructure.notifications.depends import get_notification_service
from src.infrastructure.notifications.local import MailpitNotificationService
from src.infrastructure.notifications.production import (
    ProductionNotificationInfraStructure,
)
