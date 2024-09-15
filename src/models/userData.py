from pydantic import BaseModel

from .questionData import Subjects


class User(BaseModel):
    uid: int
    username: str
    surname: str
    name: str
    lastname: str
    email: str
    region: str
    subject: Subjects
    user_class: str
    school: str
