from typing import Literal, Optional

from motor.motor_asyncio import AsyncIOMotorClientSession

from src.settings import MongoDBConfig
from src.database.mongo.session import mongo_client
from .filterRepoInterface import FilterRepoInterface
from src.models import Subjects, TrainFilterData


class FilterRepository(FilterRepoInterface):
    _database = mongo_client[MongoDBConfig.database]
    _collection = _database[MongoDBConfig.filter_collection]

    ''' Схема данных:
    {
        'uid': 12345,
        'filters': {
            'econ': {
                'question_types': [...],
                ...
            },
            'english': {
                'question_types': [...],
                ...
            }
        }
    }
    '''

    async def new(self, uid: int, subject: str, ) -> None:
        """Создать нового пользователя с пустыми фильтрами."""
        await self._collection.insert_one({
                'uid': uid,
                'filters': {
                    subject: {
                        'question_types': [],
                        'may_in_subway': [],
                        'themes': [],
                        'sources': []
                    }
                }
            },
            # session=session
        )

    async def add_subject(self, subject: Subjects, uid: int,) -> None:
        """Добавить новый предмет к фильтрам пользователя."""
        update_result = await self._collection.update_one(
            {'uid': uid},
            {
                '$set': {
                    f'filters.{subject.value}': {
                        'question_types': [],
                        'may_in_subway': [],
                        'themes': [],
                        'sources': []
                    }
                }
            },
            # session=session
        )
        if update_result.modified_count == 0:
            raise ValueError(f"Нет пользователя с uid: {uid} или предмет уже существует.")

    async def get(self, uid: int, subject: Subjects, ) -> Optional[dict]:
        """Получить фильтры пользователя по предмету."""
        user_filter = await self._collection.find_one({'uid': uid})
        if user_filter is None:
            return

        data = user_filter.get('filters', {})

        if subject.value not in data.keys():
            return

        subject_filters = data[subject.value]

        return TrainFilterData(
            question_types=subject_filters['question_types'],
            may_in_subway=subject_filters['may_in_subway'],
            themes=subject_filters['themes'],
            sources=subject_filters['sources']
        )

    async def add(
            self,
            uid: int,
            subject: Subjects,
            filter_key: Literal['question_types', 'may_in_subway', 'themes', 'sources'],
            filter_value: str,
    ) -> None:
        """Добавить фильтр пользователю по ключу. Если фильтр уже есть, то ничего не делать."""

        update_result = await self._collection.update_one(
            {'uid': uid, f'filters.{subject.value}.{filter_key}': {'$ne': filter_value}},
            {'$addToSet': {f'filters.{subject.value}.{filter_key}': filter_value}},
        )
        if update_result.matched_count == 0:
            raise ValueError(f"Не удалось добавить фильтр, проверьте uid: {uid} и предмет: {subject.value}")

    async def remove(
            self,
            uid: int,
            subject: Subjects,
            filter_key: Literal['question_types', 'may_in_subway', 'themes', 'sources'],
            filter_value: str,
    ) -> None:
        """Удалить фильтр по ключу. Если фильтр уже нет, то ничего не делать."""
        update_result = await self._collection.update_one(
            {'uid': uid, f'filters.{subject.value}.{filter_key}': filter_value},
            {'$pull': {f'filters.{subject.value}.{filter_key}': filter_value}},
        )
        if update_result.matched_count == 0:
            raise ValueError(f"Не удалось удалить фильтр, проверьте uid: {uid} и предмет: {subject.value}")
