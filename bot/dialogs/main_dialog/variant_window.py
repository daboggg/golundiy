from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from bot.state_groups import MainSG

async def on_variant_selected(callback: CallbackQuery, button: Button,
                             manager: DialogManager) -> None:
    manager.dialog_data["selected_variant"] = await button.text.render_text(manager.dialog_data, manager)
    await manager.switch_to(MainSG.get_period)

variant_window = Window(
    Const(Bold("📄 Выберите вариант:").as_html()),
    Row(
        Button(id='1', text=Const("анекдот"), on_click=on_variant_selected),
        Button(id='2', text=Const("афоризм"), on_click=on_variant_selected),
    ),
    state=MainSG.get_variant,
)
