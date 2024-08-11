from abc import ABC, abstractmethod
from typing import Optional

from src.models.userModel import User


class StatisticsRepoInterface(ABC):
    @abstractmethod
    async def create_new_user(self, session, uid):
        ...

    @abstractmethod
    async def get_user_statistics(self, session, uid) -> Optional[User]:
        ...
