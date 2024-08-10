from enum import Enum

from src.models.economics.subjectData import EconomicsData
from src.models.english.subjectData import EnglishData


class Subjects(str, Enum):
    economics = 'Экономика'
    english = 'Английский язык'


SubjectDataMapper = {
    Subjects.economics: EconomicsData(),
    Subjects.english: EnglishData()
}