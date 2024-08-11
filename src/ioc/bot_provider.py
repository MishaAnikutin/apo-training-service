from typing import AsyncIterable
from aiogram.types import TelegramObject
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database.postgres.session import new_session_maker

from src.repository.regionsRepository import RegionRepository
from src.repository.user import UserRepoInterface, UserRepository

from src.service.ValidationService import ValidationService
from src.service.UserService import UserService
from src.service.phraseService import PhraseService


class BotProvider(Provider):
    telegram_object = from_context(
        provides=TelegramObject,
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.APP)
    async def session_maker(self) -> async_sessionmaker[AsyncSession]:
        # Фабрика сессий
        return new_session_maker()

    @provide(scope=Scope.REQUEST)
    async def session(self, session_maker:  async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            try:
                yield session
                # await session.commit()

            except Exception as exc:
                # В случае ошибки откатываемся
                await session.rollback()
                raise

            finally:
                # В любом случае закрываем соединение
                await session.close()

    @provide(scope=Scope.REQUEST)
    async def user_service(
            self,
            user_repository: UserRepoInterface,
            session: AsyncSession
    ) -> UserService:
        return UserService(user_repo=user_repository, session=session)

    @provide(scope=Scope.APP)
    async def user_repository(self) -> UserRepoInterface:
        return UserRepository()

    @provide(scope=Scope.APP)
    async def region_repository(self) -> RegionRepository:
        return RegionRepository()

    @provide(scope=Scope.REQUEST)
    async def phrase_service(self) -> PhraseService:
        return PhraseService()

    @provide(scope=Scope.REQUEST)
    async def validation_service(self, region_repository: RegionRepository) -> ValidationService:
        return ValidationService(region_repository)
