from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.orm.users import UserORM
from src.models import User, Subjects, FormData
from src.repository.user import UserRepoInterface


class UserService:
    def __init__(self, user_repo: UserRepoInterface, session: AsyncSession):
        self.user_repo = user_repo
        self.session = session

    async def add_user_with_form(self, uid: int, username: str, form_data: FormData):
        async with self.session:
            await self.user_repo.add_user(
                transaction=self.session,
                user=UserORM(
                    uid=uid,
                    username=username,
                    surname=form_data.surname.name,
                    name=form_data.name.name,
                    lastname=form_data.lastname.name,
                    email=form_data.email,
                    region=form_data.region,
                    subject=form_data.main_subject,
                    user_class=form_data.training_class.status,
                    school=form_data.school
                )
            )

    async def check_user(self, uid: int):
        async with self.session:
            return await self.user_repo.get_user(uid=uid, transaction=self.session) is not None

    async def get_user(self, uid: int) -> User:
        async with self.session:
            return await self.user_repo.get_user(uid=uid, transaction=self.session)

    async def get_subject(self, uid: int) -> Subjects:
        async with self.session:
            return (await self.user_repo.get_user(uid=uid, transaction=self.session)).subject
