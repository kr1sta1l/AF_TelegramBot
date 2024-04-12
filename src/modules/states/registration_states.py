from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    EMAIL_ENTER = State()
    CODE_ENTER = State()
