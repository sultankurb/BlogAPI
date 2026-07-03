from pydantic import BaseModel


class ProfileModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    biography: str | None = None
    username: str


class ProfileUpdatedModel(ProfileModel):
    pass


class ProfileReadModel(ProfileModel):
    user_pk: int

    class Config:
        from_attributes = True
