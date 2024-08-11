from typing import Optional, AsyncIterable

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from src.repository.user import UserRepoInterface
from src.repository.orm.users import UserORM


class UserRepository(UserRepoInterface):

    async def add_user(self, transaction: AsyncSession, user: UserORM):
        print('добавляем')
        transaction.add(user)
        print('коммитим')
        await transaction.commit()

    async def get_user(self, transaction: AsyncSession, uid: int) -> Optional[UserORM]:
        user = (await transaction.execute(
            select(UserORM).where(UserORM.uid == uid).limit(1)
        )).scalar_one_or_none()

        print(f'{user = }')
        return user
