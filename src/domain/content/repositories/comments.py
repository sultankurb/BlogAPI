from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.content.schemas.comments import CommentsUpdate
from src.infrastructure.database.base_repo import BaseRepository
from src.infrastructure.database.models import CommentsORM


class CommentsRepository(BaseRepository[CommentsORM]):
    def __init__(self, session: AsyncSession ) -> None:
        super().__init__(session=session, model_cls=CommentsORM)

    async def create_comment(
            self,
            data: dict[str, Any]
    ) -> CommentsORM | None:
        comment_orm = CommentsORM(**data)
        result = await self._add(comment_orm)
        return result

    async def delete_comment(self, pk: int) -> bool:
        result = await self._delete_by_pk(pk=pk)
        return result

    async def update_comment(
            self,
            pk: int,
            data: dict[str, Any]
    ) -> CommentsORM:
        updated_comment = await self._update(
            pk=pk, data=data
        )
        return updated_comment

    async def get_by_pk(self, pk: int):
        result = await self._get_by_pk(pk=pk)
        return result

    
