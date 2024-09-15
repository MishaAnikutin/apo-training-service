from typing import Union, Optional

from src.models import QuestionData, QuestionType, Subjects
from src.repository.files.photoRepository import PhotoRepository
from .trainingSAGA import QuestionSagaOrchestrator, AnswerSagaOrchestrator
from .answerService import AnswerQuestion


class TrainingService:
    def __init__(
            self,
            question_saga: QuestionSagaOrchestrator,
            answer_saga: AnswerSagaOrchestrator,
            photo_repo: PhotoRepository
    ):
        self.question_saga = question_saga
        self.answer_saga = answer_saga
        self.photo_repo = photo_repo
        self.answer_checker = AnswerQuestion()

    async def get_random_question(self, uid: int, subject: Subjects) -> Optional[QuestionData]:
        question, question_type = await self.question_saga.execute(uid=uid, subject=subject)

        if question is None:
            return

        question_data = QuestionData(
            subject=question.subject,
            question_id=question.question_id,
            question_type=question_type,
            text=question.ask_text,
            answer_1=None if question_type in {QuestionType.yes_no, QuestionType.open} else question.answer_1,
            answer_2=None if question_type in {QuestionType.yes_no, QuestionType.open} else question.answer_2,
            answer_3=None if question_type in {QuestionType.yes_no, QuestionType.open} else question.answer_3,
            answer_4=None if question_type in {QuestionType.yes_no, QuestionType.open} else question.answer_4,
            answer_5=None if question_type in {QuestionType.yes_no, QuestionType.open} else question.answer_5,
            right_answer=question.right_answer,
            theme=question.theme,
            source=question.source,
            photo=None
        )

        if question.photo_url is not None:
            question_data.photo = await self.photo_repo.read(question_id=question.question_id, question_type=question_type)

        return question_data

    async def check_answer(
            self,
            uid: int,
            question_data:
            QuestionData,
            answer: Union[str, int],
            subject: Subjects
    ) -> bool:
        is_correct = self.answer_checker.check(question_data, answer)

        try:
            await self.answer_saga.execute(
                user_id=uid,
                question_id=question_data.question_id,
                question_type=question_data.question_type,
                theme=question_data.theme,
                is_correct=is_correct,
                subject=subject
            )

        except Exception as exc:
            await self.answer_saga.compensation(uid=uid, exc=exc)

        finally:
            return is_correct
