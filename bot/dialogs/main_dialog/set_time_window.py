from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button, Back, Next
from aiogram_dialog.widgets.text import Const, Format

from bot.action import add_task
from bot.send_message import send_message
from bot.state_groups import MainSG
from bot.utils import check_time_format, set_time_message
from database.database import set_status_active_user
from parsers.anekdot_ru import get_random_content


async def getter(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    selected_period = dialog_manager.dialog_data.get('selected_period')
    selected_variant = dialog_manager.dialog_data.get('selected_variant')
    times = dialog_manager.start_data.get('times')

    msg = set_time_message(selected_variant, selected_period, times)

    return {'msg': msg}

async def on_confirm_selected(callback: CallbackQuery, button: Button,
                             manager: DialogManager) -> None:
    await set_status_active_user(callback.from_user.id, 1)
    add_task(manager)
    await callback.answer()
    await callback.message.answer(Bold('👍Выбор сделан.\n\nЧтобы начать сначала нажмите 📋меню ➡️ выбрать контент').as_html())
    await manager.reset_stack()

async def back(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
):
    manager.start_data.get('times').clear()
    manager.start_data['count'] = 0

set_time_window = Window(
    Format(Bold("{msg}").as_html()),
    Row(
        Button(Const('Принять'), id='1', on_click=on_confirm_selected),
        Back(text=Const('🔙 назад'), on_click=back),
    ),

    state=MainSG.set_time,
    getter=getter,
)
