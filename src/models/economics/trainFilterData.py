from pydantic import BaseModel, Field

from .sourceData import EconomicsSourceData
from .themeData import EconomicsThemeData
from src.models.questionType import QuestionType


class EconomicsTrainFilterData(BaseModel):
    source:        list[EconomicsSourceData] = Field(default=[el.value for el in EconomicsSourceData])
    may_in_subway: bool                      = Field(default=True)
    question_type: list[QuestionType]        = Field(default=[el.value for el in QuestionType])
    theme:         list[EconomicsThemeData]  = Field(default=[el.value for el in EconomicsThemeData])
