from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database.postgres.session import postgres_session_maker
from src.repository import (
    PhotoRepository,
    RegionRepository,
    UserRepository, UserRepoInterface,
    FilterRepository, FilterRepoInterface,
    QuestionRepository, QuestionRepoInterface,
    StatisticsRepository, StatisticsRepoInterface,
)


class RepoProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def postgres_session_maker(self) -> async_sessionmaker[AsyncSession]:
        # Фабрика сессий
        return postgres_session_maker()

    @provide(scope=Scope.REQUEST)
    async def session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    regions = provide(RegionRepository)
    photos = provide(PhotoRepository)

    users = provide(UserRepository, provides=UserRepoInterface)
    filters = provide(FilterRepository, provides=FilterRepoInterface)
    questions = provide(QuestionRepository, provides=QuestionRepoInterface)
    statistics = provide(StatisticsRepository, provides=StatisticsRepoInterface)
