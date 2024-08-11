from typing import Union

from .economics.trainFilterData import EconomicsTrainFilterData
from .english.trainFilterData import EnglishTrainFilterData


TrainFilterData = Union[
    EconomicsTrainFilterData,
    EnglishTrainFilterData
]

