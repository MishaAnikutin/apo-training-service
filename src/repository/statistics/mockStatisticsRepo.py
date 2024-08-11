from typing import Optional

from .statisticsRepoInterface import StatisticsRepoInterface
from src.models.statisticsModel import ThemeStatisticData, StatisticsData


class MockStatisticsRepository(StatisticsRepoInterface):
    def __init__(self):
        self.users: dict[str, StatisticsData] = dict()

    async def new(self, session, uid):
        ...

    async def get(self, session, uid) -> Optional[StatisticsData]:
        ...

    async def increase_theme(self, session, uid, theme) -> None:
        ...
