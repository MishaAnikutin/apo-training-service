from pydantic import BaseModel, Field

from .themeData import EnglishThemeData


class EnglishStatisticData(BaseModel):
    theme: EnglishThemeData
    total_points: int = Field(default=0)
