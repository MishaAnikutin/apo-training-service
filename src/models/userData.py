from typing import Union
from pydantic import BaseModel

from src.models.formData import FormData
from .economics.subjectData import EconomicsData
from .english.subjectData import EnglishData


class User(BaseModel):
    uid: int
    username: str
    from_telegram: bool
    form_data: FormData
    subject_data: Union[EconomicsData, EnglishData]  # FIXME: надо иначе
