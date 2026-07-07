from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.identity.schemas.roles import RolesEnum
from src.domain.identity.schemas.users import UsersFilters, UserStatus
from src.infrastructure.database import BaseRepository
from src.infrastructure.database.models import UserRoleORM, UsersORM


class UsersRepository(BaseRepository[UsersORM]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=UsersORM)

    async def _with_roles(self, stmt):
        stmt = stmt.options(joinedload(self._model_cls.roles))
        result = await self._session.execute(stmt)
        return result.scalar()


    async def get_user_by_email(self, email: str) -> UsersORM | None:
        result = await self._get_by_filters(filed="email", value=email)
        return result

    async def get_user_by_email_with_roles(
            self,
            email: str
    ) -> UsersORM | None:
        stmt = (
            select(self._model_cls)
            .where(self._model_cls.email == email.lower())
        )
        result = await self._with_roles(stmt)
        return result

    async def get_by_pk_with_roles(self, pk: int) -> UsersORM | None:
        stmt = select(self._model_cls).where(self._model_cls.pk == pk)
        result = await self._with_roles(stmt)
        return result

    async def get_filtered_users(
        self,
        filters: UsersFilters,
        limit: int,
    ) -> Sequence[Any]:
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
        return users_db

    async def create_user(
        self,
        email: str,
        password_hash: str,
        role: int = RolesEnum.USER.value,
        status: UserStatus = UserStatus.PENDING,
    ) -> UsersORM | None:
        user_orm = UsersORM(email=email, password=password_hash, status=status)
        await self._add(user_orm)
        await self._session.execute(
            insert(UserRoleORM).values(user_pk=user_orm.pk, role_pk=role)
        )
        return user_orm

    async def get_user_by_pk(self, pk: int) -> UsersORM | None:
        user_orm = await self._get_by_pk(pk=pk)
        if user_orm is None:
            return None
        return user_orm

    async def delete_user_by_pk(self, pk: int) -> None:
        await self._delete_by_pk(pk=pk)

    async def update_user_by_pk(
        self, user_pk: int, user_data
    ) -> UsersORM | None:
        result = await self._update(pk=user_pk, data=user_data)
        return result
