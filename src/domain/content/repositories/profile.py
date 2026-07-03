from typing import Any, Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.base_repo import BaseRepository
from src.infrastructure.database.models import ProfilesORM


class ProfileRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=ProfilesORM)

    async def create_profile(
            self,
            username: str,
            user_pk: int
    ) -> ProfilesORM | None:
        orm_to_add = ProfilesORM(
            username=username,
            user_pk=user_pk,
        )
        result = await self._add(obj=orm_to_add)
        return result

    async def get_profile_by_username(
        self, username: str
    ) -> ProfilesORM | None:
        result = await self._get_by_filters(filed="username", value=username)
        return result

    async def get_profile_by_pk(self, pk: int) -> ProfilesORM | None:
        result = await self._get_by_pk(pk=pk)
        return result

    async def update_profile(
        self, pk: int, data: Mapping[str, Any]
    ) -> ProfilesORM| None:
        result = await self._update(pk=pk, data=data)
        return result
