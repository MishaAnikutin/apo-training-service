from enum import Enum


class QuestionType(str, Enum):
    yes_no = 'Задачи да/нет-ки'
    one = 'Задачи с одним вариантом ответа'
    multiple = 'Задачи с несколькими вариантами ответа'
    open = 'Задачи с открытым ответом'


matching_points = {
    QuestionType.yes_no: 1,
    QuestionType.one: 3,
    QuestionType.multiple: 5,
    QuestionType.open: 7
}