from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    username: str

class UsersBaseModel(BaseModel):
    email: EmailStr
    password: str


class UsersCreateModel(UsersBaseModel, Profile):
    pass
