from src.models.userModel import User
from .userRepoInterface import UserRepoInterface


class MockUserRepository(UserRepoInterface):
    def __init__(self):
        self.users: list[User] = list()

    async def add_user(self, user: User, session=None):
        self.users.append(user)

    async def get_user(self, uid, session=None) -> User:
        for user in self.users:
            if user.uid == uid:
                return user

        return None
