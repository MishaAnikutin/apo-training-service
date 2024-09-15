from random import choice
from typing import Optional
from sqlalchemy import select, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import QuestionType, Subjects, TrainFilterData
from src.repository.orm import question_orm_mapper, QuestionORM

from .questionRepoInterface import QuestionRepoInterface

possibleQuestionTypes = (
    QuestionType.yes_no,
    QuestionType.one,
    QuestionType.multiple,
    QuestionType.open
)


class QuestionRepository(QuestionRepoInterface):
    async def get_random_question(
            self,
            session: AsyncSession,
            subject: Subjects,
            question_types: list[QuestionType],
            user_filter: TrainFilterData
    ) -> tuple[Optional[QuestionORM], QuestionType]:
        questions = list()

        for question_type in filter(lambda x: x not in question_types, possibleQuestionTypes):
            QuestionModel = question_orm_mapper[question_type]

            questions.append((question_type, await session.scalar(
                    select(QuestionModel)
                    .where(and_(
                        QuestionModel.subject == subject,
                        QuestionModel.theme.not_in(user_filter.themes),
                        QuestionModel.source.not_in(user_filter.sources),
                        QuestionModel.may_in_subway.not_in(user_filter.may_in_subway)
                        ))
                    .order_by(func.random())
                    .limit(1)
                ))
            )

        return choice([(question, question_type)
                       for question_type, question in questions
                       if question is not None])

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
            update(QuestionModel)
            .where(QuestionModel.question_id == question_id)
            .values(number_of_decisions=QuestionModel.number_of_decisions + 1)
        )

    async def increase_number_of_right_answers(
            self,
            question_id: int,
            transaction: AsyncSession,
            question_type: QuestionType
    ) -> str:
        QuestionModel = question_orm_mapper[question_type]

        await transaction.execute(
            update(QuestionModel)
            .where(QuestionModel.question_id == question_id)
            .values(number_of_correct_decisions=QuestionModel.number_of_correct_decisions + 1)
        )
