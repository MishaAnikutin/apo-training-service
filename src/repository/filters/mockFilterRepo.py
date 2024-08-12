from src.database.mongo.session import AsyncMongoSession

from .filterRepoInterface import FilterRepoInterface


class MockFilterRepo(FilterRepoInterface):
    async def new(self, uid, session: AsyncMongoSession):
        pass

    async def get(self, uid, session: AsyncMongoSession):
        pass

    async def update(self, uid, new_filter, session: AsyncMongoSession):
        pass