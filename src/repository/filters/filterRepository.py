from typing import Literal

from motor.motor_asyncio import AsyncIOMotorClientSession

from src.settings import MongoDBConfig
from src.database.mongo.session import mongo_client

from .filterRepoInterface import FilterRepoInterface


class FilterRepository(FilterRepoInterface):
    _database = mongo_client[MongoDBConfig.database]
    _collection = _database[MongoDBConfig.filter_collection]

    '''
    Схема данных:
    
    {
        'uid': 12345,
        'filters': {
            'subjects': [...],
            'question_types': [...],
            ...
        }
    }
    '''

    async def new(self, session: AsyncIOMotorClientSession, uid: int):
        return await self._collection.insert_one({
            'uid': uid,
            'filters': {
                'subjects': [],
                'question_types': [],
                'may_in_subway': [],
                'themes': [],
                'sources': [],
            }}, session=session)

    async def get(self, session: AsyncIOMotorClientSession, uid: int):
        return await self._collection.find_one({'uid': uid}, session=session)

    async def add(
            self,
            session: AsyncIOMotorClientSession,
            uid: int,
            filter_key: Literal['subjects', 'question_types', 'may_in_subway', 'themes', 'sources'],
            filter_value: str
    ) -> None:
        """Добавить фильтр"""

        user_filters = await self._collection.find_one({'uid': uid}, session=session)

        if filter_value in user_filters[filter_key]:
            return

        user_filters[filter_key].append(filter_value)

        await self._collection.update_one({'uid': uid}, {filter_key: user_filters})

    async def remove(
            self,
            session: AsyncIOMotorClientSession,
            uid: int,
            filter_key: Literal['subjects', 'question_types', 'may_in_subway', 'themes', 'sources'],
            filter_value: str
    ) -> None:
        """Удалить фильтр"""

        user_filters = await self._collection.find_one({'uid': uid}, session=session)

        if filter_value not in user_filters[filter_key]:
            return

        user_filters[filter_key].remove(filter_value)

        await self._collection.update_one({'uid': uid}, {filter_key: user_filters})
