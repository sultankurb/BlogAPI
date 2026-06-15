from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class RoleDTO:
    pk: int
    name: str

@dataclass(frozen=True, slots=True)
class RolesFilters:
    last_pk: Optional[int]
    name: Optional[str]