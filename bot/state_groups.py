from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    get_variant = State()
    get_period = State()
    get_time = State()
    set_time = State()
    get_now = State()

class ListSubscriptionsSG(StatesGroup):
    get_subscriptions = State()
    show_subscription = State()

class AdminSG(StatesGroup):
    menu = State()
    statistics = State()
    users = State()
    user_detail = State()
