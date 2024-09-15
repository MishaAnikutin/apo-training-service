from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove

from src.controllers.train.bot.callbacks import TrainCallbacks
from src.controllers.train.bot.utils import get_response_list
from src.models import QuestionType, QuestionData


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


async def QuestionKeyboard(question: QuestionData):
    if question.question_type == QuestionType.open:
        return ReplyKeyboardRemove()

    menu_builder = ReplyKeyboardBuilder()
    answer_list = await get_response_list(question_data=question)

    for answer in answer_list:
        menu_builder.row(KeyboardButton(text=answer))

    if question.question_type == QuestionType.multiple:
        menu_builder.row(KeyboardButton(text='Ответить'))

    return menu_builder.as_markup(resize_keyboard=True)


async def ResetKeyboard():
    menu_builder = InlineKeyboardBuilder()

    menu_builder.button(text='Сбросить', callback_data=TrainCallbacks.reset_answer.value)

    return menu_builder.as_markup(resize_keyboard=True)


async def ReportKeyboard():
    menu_builder = InlineKeyboardBuilder()
    menu_builder.button(text='Ошибка в задаче?', callback_data='report')

    return menu_builder.as_markup()
