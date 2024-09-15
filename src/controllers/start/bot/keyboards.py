from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


async def startKeyboard():
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
