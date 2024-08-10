from .provider import BotProvider
from dishka import make_async_container


provider = BotProvider()
DI_Container = make_async_container(provider)

__all__ = ['DI_Container']
