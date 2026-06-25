from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.dto import UsersRoles
from src.infrastructure.database.base_repo import BaseRepository
from src.infrastructure.database.models import UserRoleORM


class UsersRolesRepository(BaseRepository[UserRoleORM, UsersRoles]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model_cls=UserRoleORM, session=session)

    @classmethod
    def _to_dto(cls, obj: UserRoleORM | None) -> UsersRoles | None:
        if obj is None:
            return None
        return UsersRoles(
            user_pk=obj.user_pk,
            role_pk=obj.role_pk
        )

    async def add_user_role(
            self,
            user_pk: int,
            role_pk: int
    ) -> None | UsersRoles:
        user_role_orm = UserRoleORM(
            user_pk=user_pk,
            role_pk=role_pk
        )
        result = await self._add(user_role_orm)
        return self._to_dto(result)
