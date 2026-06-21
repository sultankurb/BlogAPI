from typing import List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.dto import (
    UserDTO,
    UsersFilters,
    UserStatus,
    UserUpdateData,
)
from src.infrastructure.database import BaseRepository
from src.infrastructure.database.models import UsersORM


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
            status=user_orm.status
        )

    async def get_user_by_email(self, email: str) -> UserDTO | None:
       result = await self._get_by_filters(filed="email", value=email)
       return self._to_dto(result)

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
            password_hash: str
    ) -> UserDTO | None:
        user_orm = UsersORM(
            email=email,
            password=password_hash,
            status=UserStatus.PENDING
        )
        await self._add(user_orm)
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
