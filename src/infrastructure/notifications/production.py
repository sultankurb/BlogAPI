from src.infrastructure.notifications.abstract import (
    AbstractNotificationInfraStructure,
)


class ProductionNotificationInfraStructure(AbstractNotificationInfraStructure):
    async def send(
            self,
            to: str,
            title: str,
            text: str,
            from_who: str
    ) -> None:
        raise NotImplementedError()
