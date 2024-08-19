from motor.motor_asyncio import AsyncIOMotorClientSession

from .filterRepoInterface import FilterRepoInterface


class MockFilterRepo(FilterRepoInterface):
    async def new(self, uid, session: AsyncIOMotorClientSession):
        pass

    async def add(self, uid: int, filter_key: str, filter_value: str, session: AsyncIOMotorClientSession):
        pass

    async def remove(self, uid: int, filter_key: str, filter_value: str, session: AsyncIOMotorClientSession):
        pass

    async def get(self, uid, session: AsyncIOMotorClientSession):
        pass
