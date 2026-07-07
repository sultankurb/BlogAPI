from fastapi import APIRouter, status

from src.domain.content.schemas.comments import CommentsCreate, CommentsUpdate
from src.presentation.api.content.dependencies import (
    CreateCommentDepends,
    DeleteCommentDepends,
    UpdateCommentsDepends,
)
from src.presentation.api.identity.dependencies import UserDepends

comments_router = APIRouter(
    prefix="/comments",
)

@comments_router.post(
    path="/create/new/",
    status_code=status.HTTP_201_CREATED
)
async def create_new_comment(
        user: UserDepends,
        create: CreateCommentDepends,
        new_comment: CommentsCreate
):
    comment = await create.execute(
        author_pk=int(user["sub"]),
        new_comment=new_comment
    )
    return comment


@comments_router.patch(
    path="/update/{pk}",
    status_code=status.HTTP_200_OK
)
async def update_comment(
        pk: int,
        update: UpdateCommentsDepends,
        comment: CommentsUpdate,
        user: UserDepends,
):
    updated = await update.execute(pk=pk, to_update=comment, user=user)
    return updated


@comments_router.delete(
    path="/delete/{pk}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
        pk: int,
        user: UserDepends,
        delete: DeleteCommentDepends
):
    await delete.execute(pk=pk, user=user)
