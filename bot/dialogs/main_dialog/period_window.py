from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format

from bot.state_groups import MainSG


async def getter(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    return {
        'selected_variant': dialog_manager.dialog_data.get('selected_variant'),
    }


async def on_period_selected(callback: CallbackQuery, button: Button,
                              manager: DialogManager) -> None:
    print(button.widget_id)
    # manager.dialog_data["selected_variant"] = await button.text.render_text(manager.dialog_data, manager)
    await manager.switch_to(MainSG.result)


period_window = Window(
    Format("🚩 Выбран: {selected_variant}"),
    Const(Bold("📄 Выберите период:").as_html()),
    Row(
        Button(id='1', text=Const("1 раз в день"), on_click=on_period_selected),
        Button(id='2', text=Const("2 раза в день"), on_click=on_period_selected),
    ),
    state=MainSG.get_period,
    getter=getter,
)
