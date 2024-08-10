from pydantic import BaseModel, Field

from .trainFilterData import EnglishTrainFilterData
from .statisticsData import EnglishStatisticData


class EnglishData(BaseModel):
    train_filter: EnglishTrainFilterData = Field(default=EnglishTrainFilterData())
    statistics: list[EnglishStatisticData] = Field(default=None)
