from datetime import date
from .base import BaseTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, VARCHAR, Enum, DateTime

from src.models import Subjects


class UserORM(BaseTable):
    __tablename__ = 'users'

    uid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(32), unique=False, nullable=True)
    reg_date: Mapped[date] = mapped_column(DateTime, default=date.today())
    upd_date: Mapped[date] = mapped_column(DateTime, onupdate=date.today(), default=date.today())
    surname: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    lastname: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    region: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    subject: Mapped[Subjects] = mapped_column(Enum(Subjects), nullable=False)
    user_class: Mapped[str] = mapped_column(VARCHAR(10), nullable=False)
    school: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)

    def __str__(self) -> str:
        return f'<User:{self.uid}>'
