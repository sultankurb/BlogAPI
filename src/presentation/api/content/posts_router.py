from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from src.domain.content.schemas.posts import (
    PostsCreate,
    PostsFilters,
    PostsRead,
    PostsUpdate,
)
from src.presentation.api.content.dependencies import (
    CreatePostDepends,
    DeletePostDepends,
    ReadOnePostDepends,
    ReadPostsDepends,
    UpdatePostDepends,
)
from src.presentation.api.identity.dependencies import UserDepends

posts_router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@posts_router.get(path="/", response_model=List[PostsRead])
async def read_posts(
        read: ReadPostsDepends,
        posts_filters: Annotated[PostsFilters, Depends()]
):
    posts = await read.execute(posts_filters=posts_filters)
    return posts


@posts_router.get(path="/{post_pk}")
async def get_post_details(post_pk: int, read: ReadOnePostDepends):
    post = await read.execute(pk=post_pk)
    return post

@posts_router.post(
    path="/create/new/post/",
    response_model=PostsRead, 
    status_code=status.HTTP_201_CREATED
)
async def create_post(
        post: PostsCreate,
        user: UserDepends,
        create: CreatePostDepends
):
    new_post = await create.execute(data=post, author_pk=int(user["sub"]))
    return new_post


@posts_router.patch(
    path="/update/{post_pk}",
    response_model=PostsRead
)
async def update_post_by_pk(
        post_pk: int,
        post: PostsUpdate,
        user: UserDepends,
        update: UpdatePostDepends,
):
    updated_post = await update.execute(post_pk=post_pk, user=user, data=post)
    return updated_post


@posts_router.delete(
    path="/delete/{post_pk}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_from_pk(
        post_pk: int,
        user: UserDepends,
        delete: DeletePostDepends,
):
    answer = await delete.execute(post_pk=post_pk, user=user)
    return answer

