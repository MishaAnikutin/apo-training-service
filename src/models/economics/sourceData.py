from enum import Enum


class EconomicsSourceData(str, Enum):
    region: str = 'Региональный этап ВсОШ'
    zakl: str = 'Заключительный этап ВсОШ'
    vp: str = 'Высшая проба'
    sibiriada: str = 'Сибириада'
    mosh: str = 'Московская олимпиада школьников'
    ieo: str = 'IEO'
