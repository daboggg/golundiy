from aiogram.utils.formatting import Bold
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const

from bot.state_groups import MainSG

result_window = Window(
    Const(Bold("📄 Выбор сделан").as_html()),
    Const(Bold("📄 Нажмите старт").as_html()),
    state=MainSG.result
)
