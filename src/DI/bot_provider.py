from typing import AsyncGenerator

from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, Scope, from_context, provide

from src.database.postgres.session import AsyncSessionLocal

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

    @provide(scope=Scope.APP)
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with AsyncSessionLocal() as session:
            try:
                # Выполняю транзакцию
                yield session
                await session.commit()

            except Exception:
                # В случае ошибки откатываю все назад
                await session.rollback()
                raise

            finally:
                # В любом случае закрываю соединение
                await session.close()

    @provide(scope=Scope.REQUEST)
    async def user_service(self, user_repository: UserRepoInterface) -> UserService:
        return UserService(user_repo=user_repository)

    @provide(scope=Scope.APP)
    async def user_repository(self) -> UserRepoInterface:
        return MockUserRepository()

    @provide(scope=Scope.APP)
    async def region_repository(self) -> RegionRepository:
        return RegionRepository()

    @provide(scope=Scope.REQUEST)
    async def phrase_service(self) -> PhraseService:
        return PhraseService()

    @provide(scope=Scope.REQUEST)
    async def validation_service(self, region_repository: RegionRepository) -> ValidationService:
        return ValidationService(region_repository)
