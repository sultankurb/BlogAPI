from select import select
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.dto import RoleDTO, RolesFilters
from src.infrastructure.database import BaseRepository
from src.infrastructure.database.models import RolesORM


class UsersRepository(BaseRepository[RolesORM, RoleDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=RolesORM)

    @classmethod
    def _to_dto(cls, role: RolesORM) -> RoleDTO:
        return RoleDTO(
            pk=role.pk,
            name=role.name,
        )

    async def get_filtered_roles(self, filters: RolesFilters) -> List[RoleDTO]:
        stmt = select(self._model_cls)
        if filters.last_pk is not None:
            stmt = stmt.where(self._model_cls.pk < filters.last_pk)
        if filters.name is not None:
            stmt = stmt.where(self._model_cls.name == filters.name)
        result = await self._session.scalars(stmt)
        roles_db = result.all()
        return [
            RoleDTO(pk=r.pk, name=r.name)
            for r in roles_db
        ]

    async def create_role(self, name: str) -> RoleDTO:
        role_orm = RolesORM(name=name)
        await self._add(role_orm)
        return self._to_dto(role_orm)

    async def get_role_by_pk(self, pk: int) -> RoleDTO | None:
        role = await self._get_by_pk(pk=pk)
        if role is None:
            return None
        return self._to_dto(role=role)


