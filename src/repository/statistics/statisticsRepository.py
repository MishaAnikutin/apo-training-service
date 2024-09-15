from motor.motor_asyncio import AsyncIOMotorClientSession
from src.models import Subjects
from src.settings import MongoDBConfig
from src.database.mongo.session import mongo_client
from src.repository.statistics import StatisticsRepoInterface


class StatisticsRepository(StatisticsRepoInterface):
    _database = mongo_client[MongoDBConfig.database]
    _collection = _database[MongoDBConfig.statistics_collection]

    async def new(self, uid: int, subject: str) -> None:
        """Создать статистику для нового пользователя по предмету с пустой статистикой."""
        await self._collection.insert_one({
                'uid': uid,
                'subject': subject,
                'statistics': {}
            },
        )

    async def get(self, uid: int, subject: Subjects) -> dict:
        """Получить статистику пользователя по предмету."""
        user_statistics = await self._collection.find_one({'uid': uid, 'subject': subject.value})
        return user_statistics['statistics'] if user_statistics else {}

    async def update(self, uid: int, subject: Subjects, theme: str) -> None:
        """Обновить статистику по теме. Если тема отсутствует, установить значение 0 иначе увеличить на 1."""
        user_statistics = await self._collection.find_one({'uid': uid, 'subject': subject.value})

        if user_statistics is None:
            raise ValueError(f"Статистика для uid: {uid} и предмета: {subject.value} не найдена.")

        # Получаем текущее значение статистики по теме
        current_value = user_statistics['statistics'].get(theme, 0)

        # Обновляем статистику: если она существует, увеличиваем на 1, если нет - устанавливаем 0
        await self._collection.update_one(
            {'uid': uid, 'subject': subject.value},
            {'$set': {f'statistics.{theme}': current_value + 1}},
        )
