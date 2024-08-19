from aiogram.fsm.state import StatesGroup, State


class TrainingStates(StatesGroup):
    AskQuestion = State()
    AwaitAnswer = State()
    AwaitMultipleAnswer = State()
