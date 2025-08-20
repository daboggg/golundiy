from aiogram_dialog import Dialog

from bot.dialogs.main_dialog.period_window import period_window
from bot.dialogs.main_dialog.result_window import result_window
from bot.dialogs.main_dialog.variant_window import variant_window

main_dialog = Dialog(
    variant_window,
    period_window,
    result_window
)
