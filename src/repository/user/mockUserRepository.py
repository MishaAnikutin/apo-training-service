from src.models.userModel import User
from .userRepoInterface import UserRepoInterface


class MockUserRepository(UserRepoInterface):
    def __init__(self, session):
        self.users: list[User] = list()

    async def add_user(self, user: User):
        self.users.append(user)

    async def get_user(self, uid) -> User:
        for user in self.users:
            if user.uid == uid:
                return user

        return None
