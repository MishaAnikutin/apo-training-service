from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.userData import User
from src.repository.orm.users import UserORM

from .userRepoInterface import UserRepoInterface


class MockUserRepository(UserRepoInterface):
    def __init__(self, session):
        self.users: list[User] = list()

    async def add_user(self, transaction: AsyncSession, user: UserORM):
        self.users.append(user)

    async def get_user(self, transaction: AsyncSession, uid) -> Optional[UserORM]:
        for user in self.users:
            if user.uid == uid:
                return user
