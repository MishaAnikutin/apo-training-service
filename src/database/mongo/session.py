from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import MongoDBConfig


# FIXME: Нарушается паттерн репозиторий, т.к. знаем какую СУБД используем
# FIXME: Надо перенести collection в репозитории
class AsyncMongoSession:
    """
    асинхронный контекстный менеджер для MongoDB

    async with AsyncMongoSession() as session:
        await session.pub_collection.find(...)

    """
    client = AsyncIOMotorClient(MongoDBConfig.url)
    database = client[MongoDBConfig.database]
    filter_collection = database[MongoDBConfig.filter_collection]
    statistics_collection = database[MongoDBConfig.statistics_collection]


    def __init__(self):
        # Сессия БД. будет создаваться каждый раз в конструкции
        # async with AsyncMongoSession() as session ...
        self.session = None

    async def __aenter__(self):
        # Создаем сессию
        self.session = await self.client.start_session()

        # Начинаем сессию
        self.session.start_transaction()

        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Если есть ошибка, то откатывается назад
        if exc_type:
            await self.session.abort_transaction()

        # Иначе коммитим изменения
        else:
            await self.session.commit_transaction()

        # В любом случае закрываем сессию
        await self.session.end_session()
