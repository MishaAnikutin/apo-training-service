import re
from enum import Enum
from difflib import SequenceMatcher
from string import punctuation, ascii_lowercase


class Languages(str, Enum):
    rus = 'RUS'
    eng = 'ENG'


class ValidationService:
    PUNCTUATION = punctuation
    NUMBERS = list(map(str, range(0, 10)))

    a = ord('а')
    RUSSIAN_LETTERS = ''.join(
        [chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)]
    )

    ENGLISH_LETTERS = ascii_lowercase
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    min_similar_coef = 0.5

    def __init__(self, regions_repo):
        self.regions_repo = regions_repo

    def define_language(self, letter: str):
        letter = letter.strip().lower()

        rus_letters = [word for word in letter if word in self.RUSSIAN_LETTERS]
        eng_letters = [word for word in letter if word in self.ENGLISH_LETTERS]

        if len(rus_letters) > 0 and len(eng_letters) > 0:
            raise ValueError(f'Слово "{letter}" содержит буквы и Русского и Английского алфавита')

        elif len(rus_letters) > 0:
            return Languages.rus.value

        elif len(eng_letters) > 0:
            return Languages.eng.value

        else:
            raise ValueError(f'Слово "{letter}" пустое или написано другим языком')

    @staticmethod
    def _is_similar(first: str, second: str) -> float:
        return SequenceMatcher(None, first, second).ratio()

    async def validate_region(self, user_region: str):
        """
        Validate region

        Returns max similar name of Russian Federation region to the entered by user
        and raising ValueError if user region failed validation

            Красноярский край -> Красноярский край
            Дагестан -> Республика Дагестан
            Ямало Ненецкий АО -> Ямало-Ненецкий автономный округ
            анмепигртошьл -> ValueError
        """

        region_tuple = await self.regions_repo.get_all()

        similar_dict = {
            region: similar_coef
            for region, similar_coef in sorted(
                zip(region_tuple, list(
                    map(lambda region: self._is_similar(region, user_region),
                        region_tuple))
                    ),
                key=lambda item: item[1]
            )
        }

        max_similar_region, similar_coef = list(similar_dict.items())[-1]

        if similar_coef < self.min_similar_coef:
            raise ValueError('Введенный регион достаточно отличается от всех в списке административных единиц РФ,'
                       ' попробуйте перефразировать в официальном стиле')

        return max_similar_region
