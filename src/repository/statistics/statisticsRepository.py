from motor.motor_asyncio import AsyncIOMotorClientSession

from src.settings import MongoDBConfig
from src.database.mongo.session import mongo_client
from src.repository.statistics import StatisticsRepoInterface


class StatisticsRepository(StatisticsRepoInterface):
    _database = mongo_client[MongoDBConfig.database]
    _collection = _database[MongoDBConfig.statistics_collection]

    async def new(self, session: AsyncIOMotorClientSession, subject: str, uid: int):
        return await self._collection.insert_one({'uid': uid, 'subject': subject, 'statistics': dict()}, session=session)

    async def get(self, session: AsyncIOMotorClientSession, subject: str, uid: int):
        return await self._collection.find_one({'uid': uid, 'subject': subject}, session=session)

    async def update(self, session: AsyncIOMotorClientSession, uid: int, subject: str, theme: str) -> None:
        user_statistics = await self._collection.find_one({'uid': uid, 'subject': subject}, session=session)

        if theme in user_statistics['statistics'].keys():
            user_statistics['statistics'][theme] += 1

        else:
            user_statistics['statistics'][theme] = 0

        await self._collection.update_one({'uid': uid, 'subject': subject}, {'statistics': user_statistics})
