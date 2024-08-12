from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user import UserRepoInterface


class FilterService:
    def __init__(self, filter_repo: UserRepoInterface, session: AsyncSession):
        self.filter_repo = filter_repo
        self.session = session

    async def create(self, uid: int):
        ...

    # TODO: подумать как
    async def add_filter(self, uid):
        ...

    async def check_standard_filters(self, uid):
        ...
