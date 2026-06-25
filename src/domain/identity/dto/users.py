from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypedDict


class UserStatus(str, Enum):
    ACTIVE = "active"
    PENDING = "pending"
    BANNED = "banned"
    DELETED = "deleted"


@dataclass(frozen=True, slots=True)
class UserDTO:
    pk: int
    email: str
    status: UserStatus


@dataclass(frozen=True, slots=True)
class UsersFilters:
    email: Optional[str]
    status: Optional[UserStatus]
    last_seen_pk: Optional[int]



class UserUpdateData(TypedDict, total=False):
    email: str | None
    password: str | None

@dataclass(frozen=True, slots=True)
class UsersROlesDTO(UserDTO):
    password: str
    roles: list[str]