from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    ADD_FRIEND = State()
    SET_START_INTERVAL_TIME = State()
    SET_END_INTERVAL_TIME = State()
    COMPLAIN = State()
    EDIT_PROFILE = State()
