from abc import ABC, abstractmethod


class StatisticsRepoInterface(ABC):
    @abstractmethod
    async def new(self, session, subject, uid):
        ...

    @abstractmethod
    async def get(self, session, subject, uid):
        ...

    @abstractmethod
    async def update(self, session, uid, subject, theme) -> None:
        ...
