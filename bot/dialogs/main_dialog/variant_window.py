from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const

from bot.state_groups import MainSG, AdminSG
from settings import settings


async def getter(dialog_manager: DialogManager, **kwargs):
    return {
        'is_admin': settings.bots.admin_id == dialog_manager.event.from_user.id
    }

async def on_variant_selected(callback: CallbackQuery, button: Button,
                              manager: DialogManager) -> None:
    print(button.widget_id)

    if button.widget_id == 'admin':
        await manager.start(AdminSG.menu, mode=StartMode.RESET_STACK)
    else:
        manager.dialog_data["selected_variant"] = await button.text.render_text(manager.dialog_data, manager)
        await manager.switch_to(MainSG.get_period)


variant_window = Window(
    Const(Bold("❓ Что вам послать?").as_html()),
    Row(
        Button(id='admin', text=Const('💼 admin'), when='is_admin', on_click=on_variant_selected),
    ),
    Row(
        Button(id='anecdote', text=Const("анекдот"), on_click=on_variant_selected),
        Button(id='phrase', text=Const("фразу"), on_click=on_variant_selected),

    ),
    Row(
        Button(id='story', text=Const("историю"), on_click=on_variant_selected),
        Button(id='poem', text=Const("стишок"), on_click=on_variant_selected),
    ),
    Row(
        Button(id='caricature', text=Const("карикатуру"), on_click=on_variant_selected),
        Button(id='mem', text=Const("мем"), on_click=on_variant_selected),
    ),
    state=MainSG.get_variant,
    getter=getter
)
