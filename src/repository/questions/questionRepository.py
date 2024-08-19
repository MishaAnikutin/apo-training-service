from random import choice
from typing import Optional
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import QuestionType, Subjects, TrainFilterData
from src.repository.orm import question_orm_mapper, QuestionORM

from .questionRepoInterface import QuestionRepoInterface


class QuestionRepository(QuestionRepoInterface):
    async def get_random_question(
            self,
            transaction: AsyncSession,
            subject: Subjects,
            question_types: list[QuestionType],
            user_filter: TrainFilterData
    ) -> tuple[Optional[QuestionORM], QuestionType]:
        question_type = choice(question_types)
        QuestionModel = question_orm_mapper[question_type]

        question = await transaction.scalar(
            select(QuestionModel)
            .where(and_(
                QuestionModel.subject == subject,
                QuestionModel.theme.in_(user_filter.theme),
                QuestionModel.source.in_(user_filter.source),
                QuestionModel.may_in_subway.in_(user_filter.may_in_subway)
                ))
            .order_by(func.random())
            .limit(1)
        )

        return question, question_type

    async def get_answer(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType,
    ) -> str:
        QuestionModel = question_orm_mapper[question_type]

        return await transaction.scalar(
            select(QuestionModel.right_answer)
            .where(QuestionModel.question_id == question_id)
            .limit(1)
        )

    async def increase_number_of_decisions(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType
    ) -> str:
        QuestionModel = question_orm_mapper[question_type]

        await transaction.execute(
            (QuestionModel.update().
             values(number_of_decisions=QuestionModel.number_of_decisions + 1))
        )

        await transaction.commit()

    async def increase_number_of_right_answers(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType
    ) -> str:
        QuestionModel = question_orm_mapper[question_type]

        await transaction.execute(
            (QuestionModel.update().
             values(number_of_correct_decisions=QuestionModel.number_of_correct_decisions + 1))
        )

        await transaction.commit()
