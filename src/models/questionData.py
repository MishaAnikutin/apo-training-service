from enum import Enum
from pydantic import BaseModel
from typing import Union, Optional, AsyncGenerator

from .questionType import QuestionType
from .english import EnglishData, EnglishThemeData, EnglishSourceData
from .economics import EconomicsData, EconomicsSourceData, EconomicsThemeData


class Subjects(str, Enum):
    economics = 'Экономика'
    english = 'Английский язык'
    german = 'Немецкий язык'
    obzh = 'ОБЖ'
    social = 'Обществознание'


SubjectDataMapper = {
    Subjects.economics: EconomicsData(),
    Subjects.english: EnglishData()
}

ThemeData = Union[EnglishThemeData, EconomicsThemeData]
SourceData = Union[EnglishSourceData, EconomicsSourceData]


# class QuestionData(BaseModel):
#     subject: Subjects
#     question_id: int
#     question_type: QuestionType
#     text: str
#     answer_1: Optional[str]
#     answer_2: Optional[str]
#     answer_3: Optional[str]
#     answer_4: Optional[str]
#     answer_5: Optional[str]
#     right_answer: Union[str, int]
#     theme: ThemeData
#     source: SourceData

class QuestionData(BaseModel):
    subject: Subjects
    question_id: int
    question_type: QuestionType
    text: str
    answer_1: Optional[str]
    answer_2: Optional[str]
    answer_3: Optional[str]
    answer_4: Optional[str]
    answer_5: Optional[str]
    right_answer: Union[str, int]
    theme: str
    source: str
    photo: Optional[bytes]
