from aiogram.filters.state import State, StatesGroup


class FormStates(StatesGroup):
    StartForm = State()
    GetSurname = State()
    GetName = State()
    GetLastName = State()
    GetTrainingClass = State()
    GetSchool = State()
    GetRegion = State()
    GetEmail = State()
    GetMainSubject = State()
    GetPersonalData = State()
    FinalState = State()
