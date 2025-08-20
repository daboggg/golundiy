from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    get_variant = State()
    get_period = State()
    result = State()
