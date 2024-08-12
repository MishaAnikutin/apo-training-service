from aiogram.fsm.state import StatesGroup, State


class TrainingStates(StatesGroup):
    AskQuestion = State()
    WaitingAnswer = State()

    # Для ответа со множественным выбором отдельное состояние
    # Т.к. пока пользователь не нажмет на кнопку "Ответить"
    # Нужно обрабатывать его выбор
    MultipleAnswer = State()
