from aiogram_dialog import Dialog

from bot.dialogs.main_dialog.get_now_window import get_now_window
from bot.dialogs.main_dialog.period_window import period_window
from bot.dialogs.main_dialog.get_time_window import get_time_window
from bot.dialogs.main_dialog.set_time_window import set_time_window
from bot.dialogs.main_dialog.variant_window import variant_window

main_dialog = Dialog(
    variant_window,
    period_window,
    get_time_window,
    set_time_window,
    get_now_window,
)
