from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const

from bot.state_groups import MainSG, AdminSG


async def on_variant_selected(callback: CallbackQuery, button: Button,
                              manager: DialogManager) -> None:
    if button.widget_id == 'statistics':
        await manager.switch_to(AdminSG.statistics)
    elif button.widget_id == 'users':
        await manager.switch_to(AdminSG.users)
    elif button.widget_id == 'privileges':
        await manager.switch_to(AdminSG.set_privileges)


menu_window = Window(
    Const(Bold("⚖️ Сделайте выбор").as_html()),
    Button(id='statistics', text=Const('📈 статистика'), on_click=on_variant_selected, ),
    Button(id='users', text=Const('👥 пользователи'), on_click=on_variant_selected, ),
    Button(id='privileges', text=Const('👍 привилегии'), on_click=on_variant_selected, ),
    Start(text=Const('🔙назад'), id='back', state=MainSG.get_variant, mode=StartMode.RESET_STACK, data={'count': 0, 'times': []}),
    state=AdminSG.menu,
)
