from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from bot.state_groups import MainSG, AdminSG
from settings import settings


# async def getter(dialog_manager: DialogManager, **kwargs):
#     return {
#         # 'is_admin': settings.bots.admin_id == dialog_manager.event.from_user.id
#     }

async def on_variant_selected(callback: CallbackQuery, button: Button,
                              manager: DialogManager) -> None:
    if button.widget_id == 'statistics':
        await manager.switch_to(AdminSG.statistics)


menu_window = Window(
    Const(Bold("Сделайте выбор").as_html()),
    Button(id='statistics',text=Const('📈 статистика'), on_click=on_variant_selected, ),
    state=AdminSG.menu,
    # getter=getter
)
