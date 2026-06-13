from dataclasses import dataclass
from enum import Enum


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
