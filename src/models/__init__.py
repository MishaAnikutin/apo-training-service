from typing import Union

from .economics.trainFilterData import EconomicsTrainFilterData
from .english.trainFilterData import EnglishTrainFilterData

from src.models.userData import User
from src.models.Subjects import Subjects
from src.models.formData import FormData


TrainFilterData = Union[
    EconomicsTrainFilterData,
    EnglishTrainFilterData
]

__all__ = ['User', 'Subjects', 'FormData', 'TrainFilterData']
