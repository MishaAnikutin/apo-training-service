from abc import ABC, abstractmethod
from typing import Optional

from src.models.userModel import User


class UserRepoInterface(ABC):
    @abstractmethod
    async def add_user(self, session, user: User):
        ...

    @abstractmethod
    async def get_user(self, session, uid) -> Optional[User]:
        ...
