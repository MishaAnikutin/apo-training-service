from aiogram.types import TelegramObject
from dishka import Provider, from_context, Scope

from .repo_provider import RepoProvider
from .service_provider import ServiceProvider


class BotProvider(Provider, RepoProvider, ServiceProvider):
    telegram_object = from_context(
        provides=TelegramObject,
        scope=Scope.REQUEST,
    )
