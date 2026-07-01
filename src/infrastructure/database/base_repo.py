from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, Type, TypeVar

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

OrmModel = TypeVar("OrmModel")
DTO = TypeVar("DTO")


class BaseRepository(Generic[OrmModel, DTO], ABC):
    def __init__(self, session: AsyncSession, model_cls: Type[OrmModel]):
        self._session = session
        self._model_cls = model_cls

    @classmethod
    @abstractmethod
    def _to_dto(cls, obj: OrmModel | None) -> DTO | None:
        pass

    async def _scalar_one_or_none(self, stmt) -> OrmModel | None:
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def _add(self, obj: OrmModel) -> OrmModel:
        self._session.add(obj)
        await self._session.flush()
        return obj

    async def _get_by_filters(self, filed: str, value: Any) -> OrmModel | None:
        stmt = select(self._model_cls).where(
            getattr(self._model_cls, filed) == value
        )
        orm_obj = await self._scalar_one_or_none(stmt)
        return orm_obj

    async def _get_all(self):
        stmt = select(self._model_cls)
        results = await self._session.execute(stmt)
        return results.scalars().all()

    async def _get_by_pk(self, pk: int) -> OrmModel | None:
        return await self._session.get(self._model_cls, pk)

    async def _update(self, pk: int, data: Mapping[str, Any]) -> OrmModel:
        stmt = (
            update(self._model_cls)
            .where(self._model_cls.pk == pk)
            .values(**data)
            .returning(self._model_cls)
        )
        result = await self._scalar_one_or_none(stmt)
        return result

    async def _delete_by_pk(self, pk: int) -> bool:
        obj = await self._get_by_pk(pk)
        if obj:
            await self._session.delete(obj)
            await self._session.flush()
            return True
        return False
