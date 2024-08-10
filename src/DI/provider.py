from dishka import Provider, Scope, from_context, provide
from aiogram.types import TelegramObject

from src.repository.regionsRepository import RegionRepository
from src.repository.user import UserRepoInterface, MockUserRepository
from src.service.ValidationService import ValidationService
from src.service.UserService import UserService
from src.service.phraseService import PhraseService


class BotProvider(Provider):
    telegram_object = from_context(
        provides=TelegramObject,
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.REQUEST)
    def user_service(self, user_repository: UserRepoInterface) -> UserService:
        return UserService(user_repo=user_repository)

    @provide(scope=Scope.APP)
    def user_repository(self) -> UserRepoInterface:
        return MockUserRepository()

    @provide(scope=Scope.APP)
    def region_repository(self) -> RegionRepository:
        return RegionRepository()

    @provide(scope=Scope.REQUEST)
    def phrase_service(self) -> PhraseService:
        return PhraseService()

    @provide(scope=Scope.REQUEST)
    def validation_service(self, region_repository: RegionRepository) -> ValidationService:
        return ValidationService(region_repository)
