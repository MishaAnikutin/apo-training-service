from typing import Union

from src.models.economics.sourceData import EconomicsSourceData
from src.models.economics.themeData import EconomicsThemeData
from src.models.economics.trainFilterData import EconomicsTrainFilterData
from src.models.english.sourceData import EnglishSourceData

from src.models.english.themeData import EnglishThemeData
from src.models.english.trainFilterData import EnglishTrainFilterData


TrainFilterData = Union[
    EconomicsTrainFilterData,
    EnglishTrainFilterData
]

ThemeFilter = Union[
    EconomicsThemeData,
    EnglishThemeData
]

SourceFilter = Union[
    EconomicsSourceData,
    EnglishSourceData
]


