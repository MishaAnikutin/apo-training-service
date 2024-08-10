from aiogram import Router

from .middlewares import AiogramCheckUserMiddleware
from .loggingAspect import setup_logger


def register_aspects(bot_router: Router):
    setup_logger()
    bot_router.message.middleware(AiogramCheckUserMiddleware())

