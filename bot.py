import asyncio

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from dishka.integrations.aiogram import setup_dishka

from src.ioc import bot_container
from src.settings import BotConfig
from src.aspects import register_aspects
from src.database.postgres.migrations import create_tables
from src.controllers.bot_routes import bot_router, form_router


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(
        token=BotConfig.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Создаем таблицы
    await create_tables()

    # Регистрируем аспекты
    register_aspects(bot_router)

    # Регистрируем обработчики
    dp.include_router(bot_router)

    # Регистрируем роутер для регистрации (чтобы обойти Middleware)
    dp.include_router(form_router)

    # Внедряем IoC
    setup_dishka(container=bot_container, router=dp)

    try:
        await dp.start_polling(bot)

    finally:
        await bot_container.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
