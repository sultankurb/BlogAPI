from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.domain.content.schemas.profile import ProfileReadModel
from src.domain.content.schemas.comments import CommentsRead

class PostsBaseModel(BaseModel):
    title: str
    slug: str
    content: str


class PostsCreate(PostsBaseModel):
    pass


class PostsUpdate(PostsBaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None


class PostsRead(PostsBaseModel):
    pk: int
    author_pk: int
    created_at: datetime
    updated_at: datetime
    author: ProfileReadModel | None = None
    comments: List[CommentsRead] | None = None

    class Config:
        from_attributes = True


class PostsFilters(BaseModel):
    title: str | None = None
    slug: str | None = None
    author_pk: int | None = None
    last_seen_pk: int | None = None
    limit: int = 50

    class Config:
        populate_by_name = True
