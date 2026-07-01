from typing import Any, Mapping

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.content.dto import ProfileDTO
from src.infrastructure.database.base_repo import BaseRepository
from src.infrastructure.database.models import ProfilesORM


class ProfileRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model_cls=ProfilesORM)

    @classmethod
    def _to_dto(cls, obj: ProfilesORM | None) -> ProfileDTO | None:
        if obj is None:
            return None
        return ProfileDTO(
            user_pk=obj.user_pk,
            username=obj.username,
            first_name=obj.first_name,
            last_name=obj.last_name,
            biography=obj.biography,
        )

    async def create_profile(self, username: str, user_pk: int):
        orm_to_add = ProfilesORM(
            username=username,
            user_pk=user_pk,
        )
        result = await self._add(obj=orm_to_add)
        return result

    async def get_profile_by_username(
        self, username: str
    ) -> ProfileDTO | None:
        result = await self._get_by_filters(filed="username", value=username)
        return self._to_dto(obj=result)

    async def get_profile_by_pk(self, pk: int) -> ProfileDTO | None:
        result = await self._get_by_pk(pk=pk)
        return self._to_dto(obj=result)

    async def update_profile(
        self, pk: int, data: Mapping[str, Any]
    ) -> ProfileDTO | None:
        result = await self._update(pk=pk, data=data)
        return self._to_dto(obj=result)
