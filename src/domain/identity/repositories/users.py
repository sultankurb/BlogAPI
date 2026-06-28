from typing import List

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.identity.dto import (
    RolesEnum,
    UserDTO,
    UsersFilters,
    UsersROlesDTO,
    UserStatus,
    UserUpdateData,
)
from src.infrastructure.database import BaseRepository
from src.infrastructure.database.models import UserRoleORM, UsersORM


class UsersRepository(BaseRepository[UsersORM, UserDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=UsersORM)

    @classmethod
    def _to_dto(cls, user_orm: UsersORM | None) -> UserDTO | None:
        if user_orm is None:
            return None
        return UserDTO(
            pk=user_orm.pk,
            email=user_orm.email,
            status=user_orm.status,
        )

    @classmethod
    def _to_dto_with_roles(cls, user_orm: UsersORM | None) -> UserDTO | None:
        if user_orm is None:
            return None

        return UsersROlesDTO(
            pk=user_orm.pk,
            password=user_orm.password,
            email=user_orm.email,
            status=user_orm.status,
            roles=[role.name for role in user_orm.roles]
        )

    async def get_user_by_email(self, email: str) -> UserDTO | None:
       result = await self._get_by_filters(filed="email", value=email)
       return self._to_dto(result)

    async def get_user_by_email_with_roles(
            self,
            email: str
    ) -> UserDTO | None:
        stmt = (
            select(self._model_cls)
            .where(self._model_cls.email == email.lower())
            .options(joinedload(self._model_cls.roles))
        )
        result = await self._session.execute(stmt)
        return self._to_dto_with_roles(
            user_orm=result.scalars().unique().first()
        )

    async def get_filtered_users(
            self,
            filters: UsersFilters,
            limit: int,
    ) -> List[UserDTO | None]:
        stmt = select(self._model_cls).limit(limit)

        if filters.status is not None:
            stmt = stmt.where(self._model_cls.status == filters.status)

        if filters.email is not None:
            stmt = stmt.where(
                func.lower(self._model_cls.email) == filters.email.lower()
            )

        if filters.last_seen_pk is not None:
            stmt = stmt.where(self._model_cls.pk < filters.last_seen_pk)


        stmt = stmt.order_by(self._model_cls.pk.desc())
        stmt = stmt.limit(50)

        result = await self._session.scalars(stmt)
        users_db = result.all()
        return [
            self._to_dto(user_orm=u)
            for u in users_db
        ]

    async def create_user(
            self, email: str,
            password_hash: str,
            role: int = RolesEnum.USER.value,
            status: UserStatus = UserStatus.PENDING,
    ) -> UserDTO | None:
        user_orm = UsersORM(
            email=email,
            password=password_hash,
            status=status
        )
        await self._add(user_orm)
        await self._session.execute(
            insert(UserRoleORM).values(
                user_pk=user_orm.pk,
                role_pk=role
            )
        )
        return self._to_dto(user_orm)

    async def get_user_by_pk(self, pk: int) -> UserDTO | None:
        user_orm = await self._get_by_pk(pk=pk)
        if user_orm is None:
            return None
        return self._to_dto(user_orm=user_orm)

    async def delete_user_by_pk(self, pk: int) -> None:
        await self._delete_by_pk(pk=pk)

    async def update_user_by_pk(
            self,
            user_pk: int,
            user_data: UserUpdateData
    ) -> UserDTO | None:
        result = await self._update(pk=user_pk, data=user_data)
        return self._to_dto(user_orm=result)
