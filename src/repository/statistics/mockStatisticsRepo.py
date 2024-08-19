from src.models.statisticsData import StatisticsData

from .statisticsRepoInterface import StatisticsRepoInterface


class MockStatisticsRepository(StatisticsRepoInterface):
    def __init__(self):
        self.users: dict[str, StatisticsData] = dict()

    async def new(self, session, subject, uid):
        pass

    async def get(self, session, subject, uid):
        pass

    async def update(self, session, uid, subject, theme) -> None:
        pass

