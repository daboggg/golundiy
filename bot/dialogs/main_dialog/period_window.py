from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button, Back
from aiogram_dialog.widgets.text import Const, Format

from bot.send_message import send_message
from bot.state_groups import MainSG
from parsers.anekdot_ru import get_random_content


async def getter(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    return {
        'selected_variant': dialog_manager.dialog_data.get('selected_variant'),
    }


async def on_period_selected(callback: CallbackQuery, button: Button,
                             manager: DialogManager) -> None:

    manager.dialog_data["selected_period"] = int(button.widget_id)
    await manager.switch_to(MainSG.get_time)


period_window = Window(
    Format(Bold("🕊 Вышлем {selected_variant}").as_html()),
    Const(Bold("📋 Выберите период:").as_html()),
    Row(
        Button(id='1', text=Const("1️⃣ раз в день"), on_click=on_period_selected),
        Button(id='2', text=Const("2️⃣ раза в день"), on_click=on_period_selected),
    ),
    Back(text=Const('🔙 назад')),
    state=MainSG.get_period,
    getter=getter,
)
