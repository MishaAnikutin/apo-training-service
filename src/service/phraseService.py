import random


class PhraseService:
    phrases = (
            'скучал по нам?',
            'давно не виделись)',
            'скучали по тебе!',
            'как дела?',
            'как настроение?',
            'удачной тренировки)',
            'мы ждали тебя!',
            'добро пожаловать в тренажер АПО!'
        )

    def __call__(self):
        return random.choice(self.phrases)
