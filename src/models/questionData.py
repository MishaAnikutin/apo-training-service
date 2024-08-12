from enum import Enum
from typing import Union, Optional

from pydantic import BaseModel

from .english.themeData import EnglishThemeData
from .english.sourceData import EnglishSourceData
from .economics.themeData import EconomicsThemeData
from .economics.sourceData import EconomicsSourceData


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


ThemeData = Union[EnglishThemeData, EconomicsThemeData]
SourceData = Union[EnglishSourceData, EconomicsSourceData]


class QuestionData(BaseModel):
    question_id: int
    question_type: QuestionType
    text: str
    answer_1: Optional[str]
    answer_2: Optional[str]
    answer_3: Optional[str]
    answer_4: Optional[str]
    answer_5: Optional[str]
    right_answer: Union[str, int]
    theme: ThemeData
    source: SourceData
    photo_url: Optional[str]
