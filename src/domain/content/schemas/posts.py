from datetime import datetime, timezone

from pydantic import BaseModel


class PostsBaseModel(BaseModel):
    title: str
    slug: str
    content: str
    updated_at: datetime = datetime.now()


class PostsCreate(PostsBaseModel):
    created_at: datetime = datetime.now()


class PostsUpdate(PostsBaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None
    updated_at: datetime = datetime.now()


class PostsRead(PostsBaseModel):
    pk: int
    author_pk: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostsFilters(BaseModel):
    title: str | None = None
    slug: str | None = None
    author_pk: int | None = None
    last_seen_pk: int | None = None

    class Config:
        populate_by_name = True
