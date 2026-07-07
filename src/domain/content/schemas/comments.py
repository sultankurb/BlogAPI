from pydantic import BaseModel

from src.domain.content.schemas.profile import ProfileReadModel


class CommentsBaseMode(BaseModel):
    content: str
    posts_pk: int


class CommentsCreate(CommentsBaseMode):
    pass


class CommentsRead(CommentsBaseMode):
    author_pk: int
    author: ProfileReadModel

    class Config:
        from_attributes = True


class CommentsUpdate(BaseModel):
    content: str
