from sqlalchemy.ext.asyncio import AsyncSession

from src.models.filterData import ThemeFilter, SourceFilter
from src.models.questionType import QuestionType
from src.repository.filters import FilterRepoInterface


class FilterService:
    def __init__(
            self,
            filter_repo: FilterRepoInterface,
            session: AsyncSession
    ):
        self.filter_repo = filter_repo
        self.session = session

    async def create(self, uid: int):
        await self.filter_repo.new(uid=uid, session=self.session)

    async def is_standard_filters(self, uid) -> bool:
        return True

    async def add_theme_filter(self, uid, theme_filter: ThemeFilter):
        ...

    async def remove_theme_filter(self, uid, theme_filter: ThemeFilter):
        ...

    async def add_source_filter(self, uid, source_filter: SourceFilter):
        ...

    async def remove_source_filter(self, uid, source_filter: SourceFilter):
        ...

    async def add_question_type_filter(self, uid, question_type_filter: QuestionType):
        ...

    async def remove_question_type_filter(self, uid, question_type_filter: QuestionType):
        ...

    async def add_may_in_subway_filter(self, uid, may_in_subway: bool):
        ...

    async def remove_may_in_subway_filter(self, uid, may_in_subway: bool):
        ...
