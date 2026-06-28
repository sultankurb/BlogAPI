from pydantic import BaseModel


class ProfileModel(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    biograph: str | None = None
    username: str


class ProfileUpdatedModel(ProfileModel):
    pass


class ProfileReadModel(ProfileModel):
    pass
