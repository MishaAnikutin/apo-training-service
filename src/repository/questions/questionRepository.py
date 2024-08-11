from typing import Union
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TrainFilterData, Subjects
from src.models.questionType import QuestionType
from src.repository.orm import question_orm_mapper, QuestionOPENORM, QuestionMULTMORM, QuestionONEORM, QuestionYNORM
from .questionRepoInterface import QuestionRepoInterface


class QuestionRepository(QuestionRepoInterface):
    async def get_random_question(
            self,
            transaction: AsyncSession,
            subject: Subjects,
            question_type: QuestionType,
            user_filter: TrainFilterData
    ) -> Union[QuestionYNORM, QuestionOPENORM, QuestionMULTMORM, QuestionONEORM, None]:

        QuestionORM = question_orm_mapper[question_type]

        return await transaction.scalar(
            select(QuestionORM)
            .where(and_(
                QuestionORM.subject == subject,
                QuestionORM.theme.in_(user_filter.theme),
                QuestionORM.source.in_(user_filter.source),
                QuestionORM.may_in_subway.in_(user_filter.may_in_subway)
                ))
            .order_by(func.random())
            .limit(1)
        )

    async def get_answer(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType,
    ) -> str:
        QuestionORM = question_orm_mapper[question_type]

        return await transaction.scalar(
            select(QuestionORM.right_answer)
            .where(QuestionORM.question_id == question_id)
            .limit(1)
        )

    async def increase_number_of_decisions(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType
    ) -> str:
        QuestionORM = question_orm_mapper[question_type]

        await transaction.execute(
            (QuestionORM.update().
             values(number_of_decisions=QuestionORM.number_of_decisions + 1))
        )

    async def increase_number_of_right_answers(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType
    ) -> str:
        QuestionORM = question_orm_mapper[question_type]

        await transaction.execute(
            (QuestionORM.update().
             values(number_of_correct_decisions=QuestionORM.number_of_correct_decisions + 1))
        )
