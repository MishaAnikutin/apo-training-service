from typing import Union

from .economics.statisticsData import EconomicsStatisticData
from .english.statisticsData import EnglishStatisticData


ThemeStatisticData = Union[
    EconomicsStatisticData,
    EnglishStatisticData
]


StatisticsData = list[ThemeStatisticData]

__all__ = ['EconomicsStatisticData', 'EnglishStatisticData']

