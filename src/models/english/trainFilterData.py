from pydantic import BaseModel, Field

from .sourceData import EnglishSourceData
from .themeData import EnglishThemeData
from src.models.questionType import QuestionType


class EnglishTrainFilterData(BaseModel):
    source:        list[EnglishSourceData] = Field(default=[el.value for el in EnglishSourceData])
    may_in_subway: bool                    = Field(default=True)
    question_type: list[QuestionType]      = Field(default=[el.value for el in QuestionType])
    theme:         list[EnglishThemeData]  = Field(default=[el.value for el in EnglishThemeData])
