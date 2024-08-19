from typing import Optional
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import QuestionType, Subjects
from src.repository.orm.questions import QuestionORM
from src.models import TrainFilterData


class QuestionRepoInterface(ABC):
    @abstractmethod
    async def get_random_question(
            self, transaction: AsyncSession,
            subject: Subjects,
            question_types: list[QuestionType],
            user_filter: TrainFilterData
    ) -> Optional[QuestionORM]:
        ...

    @abstractmethod
    async def get_answer(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType,
    ) -> str:
        ...

    @abstractmethod
    async def increase_number_of_decisions(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType,
    ) -> str:
        ...

    @abstractmethod
    async def increase_number_of_right_answers(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType,
    ) -> str:
        ...
