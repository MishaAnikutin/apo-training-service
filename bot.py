import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from dishka.integrations.aiogram import setup_dishka

from src.DI import bot_di
from src.aspects import register_aspects
from src.events import bot_router, form_router
from src.settings import BotConfig


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=BotConfig.token)

    # Регистрируем аспекты
    register_aspects(bot_router)

    # Регистрируем обработчики
    dp.include_router(bot_router)

    # Регистрируем роутер для регистрации (чтобы обойти Middleware)
    dp.include_router(form_router)

    # Внедряем DI
    setup_dishka(bot_di, dp)

    try:
        await dp.start_polling(bot)

    finally:
        await bot_di.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
