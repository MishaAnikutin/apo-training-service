from aiogram import Router

# Сценарии использования бота
from .start.bot import start_router
from .train.bot import train_bot_router

bot_router = Router()

bot_router.include_router(start_router)
bot_router.include_router(train_bot_router)

# Регистрируется после аспектов
from .register.bot import form_router

__all__ = ('bot_router', 'form_router')
