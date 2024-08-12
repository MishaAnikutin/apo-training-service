from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove

from src.models.questionData import QuestionType


async def StartKeyboard():
    menu_builder = ReplyKeyboardBuilder()

    menu_builder.row(
        KeyboardButton(text='Начать тренировку!'),
    )

    menu_builder.row(
        KeyboardButton(text='Статистика'),
        KeyboardButton(text='Личный кабинет'),
        KeyboardButton(text='Фильтры')
    )

    return menu_builder.as_markup(resize_keyboard=True)


async def QuestionKeyboard(question_type: QuestionType, response_list: list[str]):
    menu_builder = ReplyKeyboardBuilder()

    match question_type:
        case QuestionType.yes_no:
            menu_builder.row(KeyboardButton(text='1) нет'), KeyboardButton(text='2) да'))

        case QuestionType.one:
            for response in response_list:
                menu_builder.row(KeyboardButton(text=response))

        case QuestionType.multiple:
            for response in response_list:
                menu_builder.row(KeyboardButton(text=response))

            menu_builder.row(KeyboardButton(text='Ответить'))

        case QuestionType.open:
            return ReplyKeyboardRemove()

    return menu_builder.as_markup(resize_keyboard=True)


async def ResetKeyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.button(text='Сбросить', callback_data='reset_answer')

    return menu_builder.as_markup(resize_keyboard=True)


async def ReportKeyboard():
    menu_builder = InlineKeyboardBuilder()
    menu_builder.button(text='Ошибка в задаче?', callback_data='report')

    return menu_builder.as_markup()
