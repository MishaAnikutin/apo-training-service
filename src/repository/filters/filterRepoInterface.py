from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClientSession

from src.models import Subjects


class FilterRepoInterface(ABC):
    @abstractmethod
    async def new(self, uid, subject: str, ):
        ...

    @abstractmethod
    async def add_subject(self, subject: Subjects, uid: int, ):
        ...

    @abstractmethod
    async def get(self, uid, subject: Subjects, ):
        ...

    @abstractmethod
    async def add(
            self,
            uid: int,
            subject: Subjects,
            filter_key: str,
            filter_value: str,

    ):
        ...

    @abstractmethod
    async def remove(
            self,
            uid: int,
            subject: Subjects,
            filter_key: str,
            filter_value: str,

    ):
        ...
