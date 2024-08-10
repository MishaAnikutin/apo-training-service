from pydantic import BaseModel, Field

from .themeData import EconomicsThemeData


class EconomicsStatisticData(BaseModel):
    theme: EconomicsThemeData
    total_points: int = Field(default=0)

