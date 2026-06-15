from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, Type, TypeVar

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

OrmModel = TypeVar("OrmModel")
DTO = TypeVar("DTO")

class BaseRepository(Generic[OrmModel, DTO], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[OrmModel]):
        self._session = session
        self._model_cls = model_cls


    @classmethod
    @abstractmethod
    def _to_dto(cls, obj: OrmModel) -> DTO:
        pass

    async def _add(self, obj: OrmModel) -> OrmModel:
        self._session.add(obj)
        return obj

    async def _get_by_pk(self, pk: int) -> OrmModel | None:
        return await self._session.get(self._model_cls, pk)

    async def _delete(self, obj: OrmModel) -> None:
        await self._session.delete(obj)

    async def _scalar_one_or_none(self, stmt) -> Any:
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _update_one(
            self,
            pk: int,
            update_data: Mapping[str, Any]
    ) -> DTO | None:
        stmt = (
            update(self._model_cls)
            .where(self._model_cls.pk == pk)
            .values(**update_data)
        )
        orm_obj = await self._scalar_one_or_none(stmt)
        if not orm_obj:
            return None
        return self._to_dto(obj=orm_obj)


