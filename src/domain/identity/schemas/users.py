from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    username: str

class UsersBaseModel(BaseModel):
    email: EmailStr



class UsersCreateModel(UsersBaseModel, Profile):
    password: str

class LoginSchemas(UsersBaseModel):
    password: str


class ProfileModel(Profile):
    biography: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    user_pk: int


class UserReadModel(UsersBaseModel):
    profile: ProfileModel
