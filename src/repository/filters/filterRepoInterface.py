from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClientSession


class FilterRepoInterface(ABC):
    @abstractmethod
    async def new(self, uid, session: AsyncIOMotorClientSession):
        ...

    @abstractmethod
    async def get(self, uid, session: AsyncIOMotorClientSession):
        ...

    @abstractmethod
    async def add(
            self,
            uid: int,
            filter_key: str,
            filter_value: str,
            session: AsyncIOMotorClientSession,
    ):
        ...

    @abstractmethod
    async def remove(
            self,
            uid: int,
            filter_key: str,
            filter_value: str,
            session: AsyncIOMotorClientSession,
    ):
        ...
