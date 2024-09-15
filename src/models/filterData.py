from typing import Union, Optional

from pydantic import BaseModel

from src.models.economics.sourceData import EconomicsSourceData
from src.models.economics.themeData import EconomicsThemeData
from src.models.economics.trainFilterData import EconomicsTrainFilterData
from src.models.english.sourceData import EnglishSourceData

from src.models.english.themeData import EnglishThemeData
from src.models.english.trainFilterData import EnglishTrainFilterData


# TrainFilterData = Union[
#     EconomicsTrainFilterData,
#     EnglishTrainFilterData
# ]

class TrainFilterData(BaseModel):
    question_types: list[Optional[str]]
    may_in_subway: list[Optional[str]]
    themes: list[Optional[str]]
    sources: list[Optional[str]]


ThemeFilter = Union[
    EconomicsThemeData,
    EnglishThemeData
]

SourceFilter = Union[
    EconomicsSourceData,
    EnglishSourceData
]


