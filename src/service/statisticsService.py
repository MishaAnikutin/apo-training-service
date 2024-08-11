from src.models.formModel import FormData
from src.repository.user import UserRepoInterface

from src.models.userModel import User
from src.models.Subjects import SubjectDataMapper


class StatisticsService:
    def __init__(self, statistics_repo: UserRepoInterface):
        self.user_repo = user_repo

    async def add_user_with_form(self, uid: int, username: str, form_data: FormData, from_telegram: bool):
        await self.user_repo.add_user(
            user=User(
                uid=uid,
                username=username,
                form_data=form_data,
                from_telegram=from_telegram,
                subject_data=SubjectDataMapper[form_data.main_subject]
            ),
            session=None
        )

    async def check_user(self, uid):
        return await self.user_repo.get_user(session=None, uid=uid) is not None

    async def get_user(self, uid) -> User:
        return await self.user_repo.get_user(session=None, uid=uid)
