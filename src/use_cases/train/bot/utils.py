from src.models import QuestionData, QuestionType


async def get_response_list(question_data: QuestionData) -> list[str]:
    if question_data.question_type == QuestionType.yes_no:
        return ['1) Нет', '2) Да']

    elif question_data.question_type in {QuestionType.multiple, QuestionType.one}:
        answer_list = [
            question_data.answer_1,
            question_data.answer_2,
            question_data.answer_3,
            question_data.answer_4,
            question_data.answer_5,
        ]

        return [answer for answer in answer_list if answer is not None]

    else:
        # Если множественный выбор
        return None
