from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.schemas.roles import RolesFilters
from src.infrastructure.database import BaseRepository
from src.infrastructure.database.models import RolesORM


class RolesRepository(BaseRepository[RolesORM]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=RolesORM)

    async def get_filtered_roles(
        self, filters: RolesFilters
    ) -> Sequence[Any]:
        stmt = select(self._model_cls)
        if filters.last_pk is not None:
            stmt = stmt.where(self._model_cls.pk < filters.last_pk)
        if filters.name is not None:
            stmt = stmt.where(self._model_cls.name == filters.name)
        result = await self._session.scalars(stmt)
        roles_db = result.all()
        return roles_db

    async def create_role(self, name: str) -> RolesORM | None:
        role_orm = RolesORM(name=name)
        await self._add(role_orm)
        return role_orm

    async def get_role_by_pk(self, pk: int) -> RolesORM | None:
        role = await self._get_by_pk(pk=pk)
        return role

    async def create_if_not_exists(self, role_name: str) -> None:
        stmt = insert(self._model_cls).values(name=role_name)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        await self._session.execute(stmt)

    async def delete_role(self, pk: int) -> bool:
        answer = await self._delete_by_pk(pk=pk)
        return answer

    async def get_role_by_name(self, name: str) -> RolesORM | None:
        result = await self._get_by_filters(filed="name", value=name)
        return result
