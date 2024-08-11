import datetime
from .base import BaseTable
from sqlalchemy import Column, Integer, VARCHAR, JSON, DATE, TEXT


class UserModel(BaseTable):
    __tablename__ = 'users'

    user_id = Column('uid', Integer, unique=True, nullable=False, primary_key=True)
    username = Column('username', VARCHAR(32), unique=False, nullable=True)
    reg_date = Column('registration_date', DATE, default=datetime.date.today())
    upd_date = Column('last_update_date', DATE, onupdate=datetime.date.today())
    surname = Column('surname', VARCHAR(200), nullable=False)
    name = Column('name', VARCHAR(200), nullable=False)
    lastname = Column('lastname', VARCHAR(200), nullable=False)
    email = Column('email', VARCHAR(200), nullable=False)
    region = Column('region', VARCHAR(200), nullable=False)
    subject = Column('subject', VARCHAR(200), nullable=False)
    user_class = Column('class', VARCHAR(10), nullable=False)
    school = Column('school', VARCHAR(200), nullable=False)

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'
