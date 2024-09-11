from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    get_date = State()
    set_admin = State()