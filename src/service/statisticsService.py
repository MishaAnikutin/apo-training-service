from src.models.statisticsData import StatisticsData
from src.repository.statistics import StatisticsRepoInterface


class StatisticsService:
    def __init__(self, statistics_repo: StatisticsRepoInterface, session):
        self.statistics_repo = statistics_repo
        self.session = session

    async def get_user(self, uid) -> StatisticsData:
        user_statistics = await self.statistics_repo.get(session=self.session, uid=uid)
        return

    async def get_user_top_place(self) -> int:
        """Место человека в топе"""

        return 1