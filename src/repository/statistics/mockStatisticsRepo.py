from typing import Optional

from src.models.statisticsData import StatisticsData
from .statisticsRepoInterface import StatisticsRepoInterface


class MockStatisticsRepository(StatisticsRepoInterface):
    def __init__(self):
        self.users: dict[str, StatisticsData] = dict()

    async def new(self, session, uid):
        ...

    async def get(self, session, uid) -> Optional[StatisticsData]:
        ...

    async def update(self, session, uid, theme) -> None:
        ...
