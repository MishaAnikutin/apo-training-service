from .bot_provider import BotProvider
from dishka import make_async_container


bot_di = make_async_container(BotProvider())

__all__ = ['bot_di']
