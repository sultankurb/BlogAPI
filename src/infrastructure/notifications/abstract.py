from abc import ABC, abstractmethod


class AbstractNotificationInfraStructure(ABC):
    @classmethod
    @abstractmethod
    async def send(
            cls,
            to: str,
            title: str,
            text: str,
            from_who: str
    ) -> None:
        raise NotImplementedError
