from src.models.statisticsData import StatisticsData
from src.repository.statistics import StatisticsRepoInterface


class StatisticsService:
    def __init__(self, statistics_repo: StatisticsRepoInterface):
        self.statistics_repo = statistics_repo

    async def new(self, uid, subject: str):
        await self.statistics_repo.new(uid=uid, subject=subject)

    async def get_user(self, uid, subject: str) -> StatisticsData:
        return await self.statistics_repo.get(uid=uid, subject=subject)

    async def get_user_top_place(self) -> int:
        """Место человека в топе"""

        return 1