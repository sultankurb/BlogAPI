from typing import Annotated

from fastapi import Depends

from src.domain.content.use_cases import ProfilesUpdateUseCase
from src.domain.content.use_cases.comments import (
    CommentsCreateUseCase,
    CommentsDeleteUsaCase,
    CommentsUpdateUsaCase,
)
from src.domain.content.use_cases.posts import (
    PostCreateUseCase,
    PostDeleteUseCase,
    PostUpdateUseCase,
    ReadOnePostUseCase,
    ReadPostsUseCase,
)
from src.domain.content.use_cases.uow import ContentUow
from src.infrastructure.database import session_factory


def get_content_uow():
    return ContentUow(session=session_factory)

ContentUowDep = Annotated[ContentUow, Depends(get_content_uow)]


def get_profile_update(uow: ContentUowDep) -> ProfilesUpdateUseCase:
    return ProfilesUpdateUseCase(uow=uow)


ProfileUpdateDepends = Annotated[
    ProfilesUpdateUseCase, Depends(get_profile_update)
]

def read_all_posts(uow: ContentUowDep) -> ReadPostsUseCase:
    return ReadPostsUseCase(uow=uow)

ReadPostsDepends = Annotated[ReadPostsUseCase, Depends(read_all_posts)]

def read_one_post(uow: ContentUowDep) -> ReadOnePostUseCase:
    return ReadOnePostUseCase(uow=uow)

ReadOnePostDepends = Annotated[ReadOnePostUseCase, Depends(read_one_post)]

def create_new_post(uow: ContentUowDep) -> PostCreateUseCase:
    return PostCreateUseCase(uow=uow)

CreatePostDepends = Annotated[PostCreateUseCase, Depends(create_new_post)]

def delete_one_post(uow: ContentUowDep) -> PostDeleteUseCase:
    return PostDeleteUseCase(uow=uow)

DeletePostDepends = Annotated[PostDeleteUseCase, Depends(delete_one_post)]


def update_one_post(uow: ContentUowDep) -> PostUpdateUseCase:
    return PostUpdateUseCase(uow=uow)

UpdatePostDepends = Annotated[PostUpdateUseCase, Depends(update_one_post)]


def create_new_comments(uow: ContentUowDep) -> CommentsCreateUseCase:
    return CommentsCreateUseCase(uow=uow)

CreateCommentDepends = Annotated[
    CommentsCreateUseCase,
    Depends(create_new_comments)
]

def delete_comments(uow: ContentUowDep) -> CommentsDeleteUsaCase:
    return CommentsDeleteUsaCase(uow=uow)

DeleteCommentDepends = Annotated[
    CommentsDeleteUsaCase,
    Depends(delete_comments)
]

def update_comments(uow: ContentUowDep) -> CommentsUpdateUsaCase:
    return CommentsUpdateUsaCase(uow=uow)

UpdateCommentsDepends = Annotated[
    CommentsUpdateUsaCase,
    Depends(update_comments)
]
