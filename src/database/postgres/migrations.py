from .session import engine
from src.repository.orm.base import BaseTable


async def create_tables():
    async with engine.begin() as conn:
        # Создаем все таблицы
        await conn.run_sync(BaseTable.metadata.create_all)
