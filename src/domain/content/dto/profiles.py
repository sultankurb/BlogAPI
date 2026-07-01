from dataclasses import dataclass
from typing import Optional, TypedDict


@dataclass(frozen=True, slots=True)
class ProfileDTO:
    user_pk: int
    username: str
    first_name: str | None
    last_name: str | None
    biography: str | None


@dataclass(frozen=True, slots=True)
class ProfileFilter:
    user_pk: Optional[int]
    username: Optional[str]


class ProfileDataUpdate(TypedDict, total=False):
    user_pk: int
    username: str
    first_name: str
    last_name: str
    biography: str
