from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from src.models.Subjects import Subjects


async def subjectsKeyboard():
    menu_builder = ReplyKeyboardBuilder()
    subject_list = [subject.value for subject in Subjects]

    for subject in subject_list:
        menu_builder.button(text=subject)

    return menu_builder.as_markup(resize_keyboard=True)


async def yesNoKeyboard():
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.row(KeyboardButton(text='Да'), KeyboardButton(text='Нет'))
    return menu_builder.as_markup(resize_keyboard=True)
