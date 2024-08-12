from typing import Union

from src.models.questionData import QuestionData
from .trainingSAGA import QuestionSagaOrchestrator, AnswerSagaOrchestrator


class TrainingService:
    def __init__(
            self,
            question_saga: QuestionSagaOrchestrator,
            answer_saga: AnswerSagaOrchestrator
    ):
        self.question_saga = question_saga
        self.answer_saga = answer_saga

    async def get_random_question(self, uid) -> QuestionData:
        try:
            question = await self.question_saga.execute(uid=uid)

        except Exception as exc:
            await self.question_saga.compensation(uid=uid, exc=exc)

        # TODO
        return QuestionData()

    async def _is_correct(self, question_data: QuestionData, answer: Union[str, int]) -> bool:
        # TODO
        return True

    async def check_answer(self, uid: int, question_data: QuestionData, answer: Union[str, int]):
        try:
            await self.answer_saga.execute(
                user_id=uid,
                question_id=question_data.question_id,
                question_type=question_data.question_type,
                theme=question_data.theme,
                is_correct=await self._is_correct(question_data=question_data, answer=answer)
            )

        except Exception as exc:
            await self.answer_saga.compensation(uid=uid, exc=exc)
