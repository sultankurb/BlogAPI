from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypedDict


@dataclass(frozen=True, slots=True)
class PostsCreateDTO:
    title: str
    slug: str
    content: str
    author_pk: int
    created_at: datetime
    updated_at: datetime

@dataclass(frozen=True, slots=True)
class PostsFilter:
    title: str
    slug: str
    author_pk: int
    last_seen_pk: int

class PostsDataUpdate(TypedDict, total=False):
    title: str
    slug: str
    content: str
    updated_at: datetime

@dataclass(frozen=True, slots=True)
class PostsReadDTO(PostsCreateDTO):
    pk: int
