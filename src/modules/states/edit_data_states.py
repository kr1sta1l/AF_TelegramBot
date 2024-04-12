from aiogram.fsm.state import State, StatesGroup


class EditDataStates(StatesGroup):
    NAME_ENTER = State()
    CONFIRMATION = State()
    MAIN_MENU = State()
