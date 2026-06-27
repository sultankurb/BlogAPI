from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass(frozen=True, slots=True)
class RoleDTO:
    pk: int
    name: str

@dataclass(frozen=True, slots=True)
class RolesFilters:
    last_pk: Optional[int]



class RolesEnum(Enum):
    USER = 1
    ADMIN = 2
    MODERATOR = 3
