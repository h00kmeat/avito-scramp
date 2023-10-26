from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    choosing_buttons = State()
    waiting_to_be_created = State()
    waiting_to_update = State()
