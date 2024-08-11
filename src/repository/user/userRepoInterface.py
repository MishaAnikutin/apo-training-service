from typing import Optional
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.userModel import User
from src.repository.orm.users import UserORM


class UserRepoInterface(ABC):
    @abstractmethod
    async def add_user(self, transaction: AsyncSession, user: UserORM):
        ...

    @abstractmethod
    async def get_user(self, transaction: AsyncSession, uid) -> Optional[UserORM]:
        ...
