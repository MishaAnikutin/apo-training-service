from abc import ABC, abstractmethod
from typing import Optional


# TODO
class StatisticsRepoInterface(ABC):
    @abstractmethod
    async def new(self, session, uid):
        ...

    @abstractmethod
    async def get(self, session, uid):
        ...

    @abstractmethod
    async def update(self, session, uid, theme) -> None:
        ...
