from typing import Union

from src.models import QuestionData, QuestionType


class AnswerQuestion:
    def check(
            self,
            question_data: QuestionData,
            user_answer: Union[str, int, list[int]]
    ) -> bool:
        match question_data.question_type:
            case QuestionType.yes_no:
                return self._is_correct_yesno(question_data=question_data, user_answer=user_answer)
            case QuestionType.one:
                return self._is_correct_one(question_data=question_data, user_answer=user_answer)
            case QuestionType.multiple:
                return self._is_correct_mult(question_data=question_data, user_answer=user_answer)
            case QuestionType.open:
                return self._is_correct_open(question_data=question_data, user_answer=user_answer)

    @staticmethod
    def _is_correct_yesno(question_data: QuestionData, user_answer: int):
        return question_data.right_answer == user_answer

    def _is_correct_one(self, question_data: QuestionData, user_answer: int):
        ...

    def _is_correct_mult(self, question_data: QuestionData, user_answer: list[int]):
        ...

    def _is_correct_open(self, question_data: QuestionData, user_answer: str):
        ...
