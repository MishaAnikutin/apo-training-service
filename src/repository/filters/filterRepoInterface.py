from abc import ABC, abstractmethod

from src.database.mongo.session import AsyncMongoSession


class FilterRepoInterface(ABC):
    @abstractmethod
    async def new(self, uid, session: AsyncMongoSession):
        ...

    @abstractmethod
    async def get(self, uid, session: AsyncMongoSession):
        ...

    @abstractmethod
    async def update(self, uid, new_filter, session: AsyncMongoSession):
        ...
