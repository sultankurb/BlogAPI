from src.infrastructure.notifications.abstract import (
    AbstractNotificationInfraStructure,
)


class ProductionNotificationInfraStructure(AbstractNotificationInfraStructure):
    @classmethod
    async def send(
            cls,
            to: str,
            title: str,
            text: str,
            from_who: str
    ) -> None:
        raise NotImplementedError()
