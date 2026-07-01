from abc import ABC, abstractmethod


class AbstractNotificationInfraStructure(ABC):
    @abstractmethod
    async def send(
        self, to: str, title: str, text: str, from_who: str
    ) -> None:
        raise NotImplementedError
