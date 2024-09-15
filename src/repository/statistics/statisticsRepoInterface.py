from abc import ABC, abstractmethod


class StatisticsRepoInterface(ABC):
    @abstractmethod
    async def new(self, subject, uid):
        ...

    @abstractmethod
    async def get(self, subject, uid):
        ...

    @abstractmethod
    async def update(self, uid, subject, theme) -> None:
        ...
