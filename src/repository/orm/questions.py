from .base import BaseTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, VARCHAR, Enum, String

from src.models.Subjects import Subjects


class QuestionYNORM(BaseTable):
    __tablename__ = 'question_yes_no'

    question_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False, primary_key=True, autoincrement=True)
    ask_text: Mapped[str] = mapped_column(VARCHAR(4096), nullable=False)
    right_answer: Mapped[bool] = mapped_column(Boolean, nullable=False)
    subject: Mapped[Subjects] = mapped_column(Enum(Subjects), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    may_in_subway: Mapped[bool] = mapped_column(Boolean, nullable=False)
    have_photo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    number_of_decisions: Mapped[int] = mapped_column(Integer, default=0)
    number_of_correct_decisions: Mapped[int] = mapped_column(Integer, default=0)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:{self.question_id}>'


class QuestionONEORM(BaseTable):
    __tablename__ = 'question_one'

    question_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False,
                                             primary_key=True, autoincrement=True)

    ask_text: Mapped[str] = mapped_column(VARCHAR(4096), nullable=False)
    answer_1: Mapped[str] = mapped_column(String, nullable=False)
    answer_2: Mapped[str] = mapped_column(String, nullable=False)
    answer_3: Mapped[str] = mapped_column(String, nullable=False)
    answer_4: Mapped[str] = mapped_column(String, nullable=False)
    answer_5: Mapped[str] = mapped_column(String, nullable=False)
    right_answer: Mapped[bool] = mapped_column(Integer, nullable=False)
    subject: Mapped[Subjects] = mapped_column(Enum(Subjects), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    may_in_subway: Mapped[bool] = mapped_column(Boolean, nullable=False)
    have_photo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    number_of_decisions: Mapped[int] = mapped_column(Integer, default=0)
    number_of_correct_decisions: Mapped[int] = mapped_column(Integer, default=0)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:{self.question_id}>'


class QuestionMULTMORM(BaseTable):
    __tablename__ = 'question_mult'

    question_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False,
                                             primary_key=True, autoincrement=True)

    ask_text: Mapped[str] = mapped_column(VARCHAR(4096), nullable=False)
    answer_1: Mapped[str] = mapped_column(String, nullable=False)
    answer_2: Mapped[str] = mapped_column(String, nullable=False)
    answer_3: Mapped[str] = mapped_column(String, nullable=False)
    answer_4: Mapped[str] = mapped_column(String, nullable=False)
    answer_5: Mapped[str] = mapped_column(String, nullable=False)
    right_answer: Mapped[bool] = mapped_column(VARCHAR(30), nullable=False)
    subject: Mapped[Subjects] = mapped_column(Enum(Subjects), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    may_in_subway: Mapped[bool] = mapped_column(Boolean, nullable=False)
    have_photo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    number_of_decisions: Mapped[int] = mapped_column(Integer, default=0)
    number_of_correct_decisions: Mapped[int] = mapped_column(Integer, default=0)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:{self.question_id}>'


class QuestionOPENORM(BaseTable):
    __tablename__ = 'question_open'

    question_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False,
                                             primary_key=True, autoincrement=True)

    ask_text: Mapped[str] = mapped_column(VARCHAR(4096), nullable=False)
    right_answer: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[Subjects] = mapped_column(Enum(Subjects), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    may_in_subway: Mapped[bool] = mapped_column(Boolean, nullable=False)
    have_photo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    number_of_decisions: Mapped[int] = mapped_column(Integer, default=0)
    number_of_correct_decisions: Mapped[int] = mapped_column(Integer, default=0)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}:{self.question_id}>'
