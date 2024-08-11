from enum import Enum

from src.models.economics.subjectData import EconomicsData
from src.models.english.subjectData import EnglishData


class Subjects(str, Enum):
    economics = 'Экономика'
    english = 'Английский язык'
    german = 'Немецкий язык'
    obzh = 'ОБЖ'
    social = 'Обществознание'


SubjectDataMapper = {
    Subjects.economics: EconomicsData(),
    Subjects.english: EnglishData()
}