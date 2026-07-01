from select import select
from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.dto import RoleDTO, RolesFilters
from src.infrastructure.database import BaseRepository
from src.infrastructure.database.models import RolesORM


class RolesRepository(BaseRepository[RolesORM, RoleDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=RolesORM)

    @classmethod
    def _to_dto(cls, role: RolesORM | None) -> RoleDTO | None:
        if role is None:
            return None

        return RoleDTO(
            pk=role.pk,
            name=role.name,
        )

    async def get_filtered_roles(
        self, filters: RolesFilters
    ) -> List[RoleDTO] | None:
        stmt = select(self._model_cls)
        if filters.last_pk is not None:
            stmt = stmt.where(self._model_cls.pk < filters.last_pk)
        if filters.name is not None:
            stmt = stmt.where(self._model_cls.name == filters.name)
        result = await self._session.scalars(stmt)
        roles_db = result.all()
        return [RoleDTO(pk=r.pk, name=r.name) for r in roles_db]

    async def create_role(self, name: str) -> RoleDTO | None:
        role_orm = RolesORM(name=name)
        await self._add(role_orm)
        return self._to_dto(role_orm)

    async def get_role_by_pk(self, pk: int) -> RoleDTO | None:
        role = await self._get_by_pk(pk=pk)
        return self._to_dto(role=role)

    async def create_if_not_exists(self, role_name: str) -> None:
        stmt = insert(self._model_cls).values(name=role_name)
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        await self._session.execute(stmt)

    async def delete_role(self, pk: int) -> bool:
        answer = await self._delete_by_pk(pk=pk)
        return answer

    async def get_role_by_name(self, name: str) -> RoleDTO | None:
        result = await self._get_by_filters(filed="name", value=name)
        return self._to_dto(result)
