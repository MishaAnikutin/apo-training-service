from typing import AsyncIterable

from aiogram.types import TelegramObject
from dishka import Provider, Scope, from_context, provide
from motor.motor_asyncio import AsyncIOMotorClientSession
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database.mongo.session import mongo_client
from src.database.postgres.session import postgres_session_maker

from src.repository.files import PhotoRepository
from src.repository.questions import QuestionRepoInterface
from src.repository.questions.questionRepository import QuestionRepository
from src.repository.statistics import StatisticsRepoInterface
from src.repository.regionsRepository import RegionRepository
from src.repository.statistics.statisticsRepository import StatisticsRepository
from src.repository.user import UserRepoInterface, UserRepository
from src.repository.filters import MockFilterRepo, FilterRepoInterface

from src.service.UserService import UserService
from src.service.filterService import FilterService
from src.service.phraseService import PhraseService
from src.service.validationService import ValidationService
from src.service.training.trainingService import TrainingService, AnswerSagaOrchestrator, QuestionSagaOrchestrator


# TODO: перенести зависимость сессии в репозитории
class BotProvider(Provider):
    telegram_object = from_context(
        provides=TelegramObject,
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.APP)
    async def session_maker(self) -> async_sessionmaker[AsyncSession]:
        # Фабрика сессий
        return postgres_session_maker()

    @provide(scope=Scope.REQUEST)
    async def session(self, session_maker:  async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def mongo_client(self) -> AsyncIterable[AsyncIOMotorClientSession]:
        async with await mongo_client.start_session() as session:
            yield session

    @provide(scope=Scope.APP)
    async def user_repository(self) -> UserRepoInterface:
        return UserRepository()

    @provide(scope=Scope.APP)
    async def region_repository(self) -> RegionRepository:
        return RegionRepository()

    @provide(scope=Scope.APP)
    async def filter_repository(self) -> FilterRepoInterface:
        return MockFilterRepo()

    @provide(scope=Scope.APP)
    async def photo_repository(self) -> PhotoRepository:
        return PhotoRepository()

    @provide(scope=Scope.APP)
    async def question_repository(self) -> QuestionRepoInterface:
        return QuestionRepository()

    @provide(scope=Scope.REQUEST)
    async def statistics_repository(self) -> StatisticsRepoInterface:
        return StatisticsRepository()

    @provide(scope=Scope.REQUEST)
    async def user_service(self, user_repository: UserRepoInterface, session: AsyncSession) -> UserService:
        return UserService(user_repo=user_repository, session=session)

    @provide(scope=Scope.REQUEST)
    async def filter_service(
            self,
            filter_repo: FilterRepoInterface,
            session: AsyncIOMotorClientSession
    ) -> FilterService:
        return FilterService(filter_repo=filter_repo, session=session)

    @provide(scope=Scope.REQUEST)
    async def phrase_service(self) -> PhraseService:
        return PhraseService()

    @provide(scope=Scope.REQUEST)
    async def validation_service(self, region_repository: RegionRepository) -> ValidationService:
        return ValidationService(region_repository)

    @provide(scope=Scope.REQUEST)
    async def answer_saga(
            self,
            postgres_session: AsyncSession,
            mongo_session: AsyncIOMotorClientSession,
            user_repo: UserRepoInterface,
            question_repo: QuestionRepoInterface,
            statistics_repo: StatisticsRepoInterface
    ) -> AnswerSagaOrchestrator:
        return AnswerSagaOrchestrator(
            postgres_session=postgres_session,
            mongo_session=mongo_session,
            question_repo=question_repo,
            statistics_repo=statistics_repo,
            user_repo=user_repo
        )

    @provide(scope=Scope.REQUEST)
    async def question_saga(
            self,
            postgres_session: AsyncSession,
            mongo_session: AsyncIOMotorClientSession,
            filter_repo: FilterRepoInterface,
            question_repo: QuestionRepoInterface,
            user_repo: UserRepoInterface
    ) -> QuestionSagaOrchestrator:
        return QuestionSagaOrchestrator(
            postgres_session=postgres_session,
            mongo_session=mongo_session,
            filter_repo=filter_repo,
            question_repo=question_repo,
            user_repo=user_repo
        )

    @provide(scope=Scope.REQUEST)
    async def training_service(
            self,
            answer_saga: AnswerSagaOrchestrator,
            question_saga: QuestionSagaOrchestrator,
            photo_repo: PhotoRepository
    ) -> TrainingService:
        return TrainingService(question_saga=question_saga, answer_saga=answer_saga, photo_repo=photo_repo)
