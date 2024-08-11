from typing import AsyncIterable
from aiogram.types import TelegramObject
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.repository.regionsRepository import RegionRepository
from src.repository.user import UserRepoInterface, MockUserRepository

from src.service.ValidationService import ValidationService
from src.service.UserService import UserService
from src.service.phraseService import PhraseService

from src.settings import DatabaseConfig


class BotProvider(Provider):
    telegram_object = from_context(
        provides=TelegramObject,
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.APP)
    async def session_maker(self) -> async_sessionmaker[AsyncSession]:
        # Фабрика сессий
        return async_sessionmaker(
            bind=create_async_engine(
                url=DatabaseConfig.url_str,
                echo=True,
                pool_pre_ping=True
            ),
            expire_on_commit=False,
            class_=AsyncSession
        )

    @provide(scope=Scope.APP)
    async def session(self, session_maker:  async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
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
