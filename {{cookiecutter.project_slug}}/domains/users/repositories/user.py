from dataclasses import dataclass
from typing import ClassVar, Type

from chassis.repository import BaseRepository
from domains.users.models.user import User


@dataclass
class UserRepository(BaseRepository):
    model: ClassVar[Type[User]] = User
