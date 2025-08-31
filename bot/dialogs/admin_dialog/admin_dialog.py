from aiogram_dialog import Dialog

from bot.dialogs.admin_dialog.menu_window import menu_window
from bot.dialogs.admin_dialog.statistics_window import statistics_window

admin_dialog = Dialog(
    menu_window,
    statistics_window,
)
