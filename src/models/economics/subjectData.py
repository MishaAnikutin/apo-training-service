from pydantic import BaseModel, Field

from .trainFilterData import EconomicsTrainFilterData
from .statisticsData import EconomicsStatisticData


class EconomicsData(BaseModel):
    train_filter: EconomicsTrainFilterData = Field(default=EconomicsTrainFilterData())
    statistics:   list[EconomicsStatisticData]   = Field(default=None)
