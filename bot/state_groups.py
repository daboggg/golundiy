from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    get_variant = State()
    get_period = State()
    get_time = State()
    set_time = State()
    confirm = State()

class ListSubscriptionsSG(StatesGroup):
    get_subscriptions = State()
    show_subscription = State()
