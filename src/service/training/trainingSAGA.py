import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.models import TrainFilterData, QuestionType
from src.models.questionData import ThemeData

from src.repository.orm import QuestionORM
from src.repository.user import UserRepoInterface
from src.repository.filters import FilterRepoInterface
from src.repository.questions import QuestionRepoInterface
from src.repository.statistics import StatisticsRepoInterface

from .sagaInterface import SAGAInterface

logger = logging.getLogger(__name__)


class QuestionSagaOrchestrator(SAGAInterface):
    def __init__(
            self,
            postgres_session: AsyncSession,
            mongo_session: AsyncIOMotorClientSession,
            filter_repo: FilterRepoInterface,
            question_repo: QuestionRepoInterface,
            user_repo: UserRepoInterface
    ):
        self._user_repo = user_repo
        self._filter_repo = filter_repo
        self._question_repo = question_repo

        self._mongo_session = mongo_session
        self._postgres_session = postgres_session

    async def execute(self, uid: int) -> tuple[Optional[QuestionORM], QuestionType]:
        # Получаем фильтры пользователя
        async with self._mongo_session as session:
            logger.info(f"[SAGA] {uid=} получаем фильтры")
            user_filters: TrainFilterData = await self._filter_repo.get(uid=uid, session=session)

            if user_filters is None:
                await self._filter_repo.new(uid=uid, session=session)
                user_filters: TrainFilterData = await self._filter_repo.get(uid=uid, session=session)

        # Получаем предмет пользователя и случайный вопрос
        async with self._postgres_session as transaction:
            logger.info(f"[SAGA] {uid=} получаем предмет")
            subject = (await self._user_repo.get_user(transaction=transaction, uid=uid)).subject

            logger.info(f"[SAGA] {uid=} получаем случайный вопрос для")
            random_question = (await self._question_repo
                               .get_random_question(
                                    transaction=self._postgres_session,
                                    subject=subject,
                                    question_types=user_filters.question_type,
                                    user_filter=user_filters))

            return random_question

    async def compensation(self, uid, exc):
        # TODO: надо подумать что делать в случае ошибки
        logger.error(f"[SAGA] {uid=} ошибка получения вопроса {exc}")


class AnswerSagaOrchestrator(SAGAInterface):
    def __init__(
            self,
            user_repo: UserRepoInterface,
            question_repo: QuestionRepoInterface,
            statistics_repo: StatisticsRepoInterface,
            postgres_session: AsyncSession,
            mongo_session: AsyncIOMotorClientSession

    ):
        self._user_repo = user_repo
        self._question_repo = question_repo
        self._statistics_repo = statistics_repo

        self._mongo_session = mongo_session
        self._postgres_session = postgres_session

    async def execute(
            self,
            user_id: int,
            question_id: int,
            question_type: QuestionType,
            theme: ThemeData,
            is_correct: bool
    ) -> None:
        async with self._postgres_session as session:
            # Обновляем статистику верных ответов
            if is_correct:
                (await self._question_repo
                 .increase_number_of_right_answers(
                    question_id=question_id,
                    question_type=question_type,
                    transaction=session))

            # Обновляем статистику суммарных ответов
            (await self._question_repo
             .increase_number_of_decisions(
                question_id=question_id,
                question_type=question_type,
                transaction=session
            ))

        # Обновляем статистику пользователя
        async with self._mongo_session as session:
            (await self._statistics_repo.update(session=session, uid=user_id, theme=theme))

    async def compensation(self, uid, exc):
        logger.error(f"[SAGA] {uid=} ошибка получения вопроса {exc}")
        await self._postgres_session.rollback()
