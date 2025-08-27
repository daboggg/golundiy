from aiogram_dialog import Dialog

from bot.dialogs.list_subscriptions_dialog.get_subscriptions_window import get_subscriptions_window
from bot.dialogs.list_subscriptions_dialog.show_subscribe_window import show_subscribe_window

list_subscriptions_dialog = Dialog(
    get_subscriptions_window,
    show_subscribe_window,
)
