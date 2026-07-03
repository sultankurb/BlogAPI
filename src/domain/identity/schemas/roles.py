from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RolesEnum(Enum):
    USER = 1
    ADMIN = 2
    MODERATOR = 3

class RolesFilters(BaseModel):
    last_pk: Optional[int]
    name: Optional[str]
