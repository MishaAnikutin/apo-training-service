from abc import ABC, abstractmethod
from typing import Optional

from src.models.userModel import User


class StatisticsRepoInterface(ABC):
    @abstractmethod
    async def new(self, session, uid):
        ...

    @abstractmethod
    async def get(self, session, uid) -> Optional[User]:
        ...

    @abstractmethod
    async def increase_theme(self, session, uid, theme) -> None:
        ...
