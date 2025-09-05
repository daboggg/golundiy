import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, SwitchTo, Multiselect, Column, ManagedMultiselect
from aiogram_dialog.widgets.text import Format, Const

from bot.state_groups import AdminSG
from database.database import get_users, is_privileged_user, set_privileged_status


async def getter(dialog_manager: DialogManager, **kwargs):
    multiselect: ManagedMultiselect = dialog_manager.find("users_p")
    all_users = await get_users()

    user_list = []
    for user in all_users:
        name: str = user[2] if not user[3] else f'{user[2]} {user[3]}'
        user_id: str = str(user[1])
        user_list.append((name, user_id,))
        if user[7] == 1:
            await multiselect.set_checked(user_id, checked=True)

    return {
        "user_list": user_list,
        "count": len(user_list),
    }


async def on_click(callback: CallbackQuery, select: ManagedMultiselect, manager: DialogManager, data) -> None:
    if await is_privileged_user(int(data)):
        await set_privileged_status(int(data), 0)
    else:
        await set_privileged_status(int(data), 1)


set_privileges_window = Window(
    Const("👍 привилегии"),

    ScrollingGroup(
        Column(
            Multiselect(
                Format("☑️  {item[0]}"),  # E.g `✓ Apple`
                Format("🔲  {item[0]}"),
                id="users_p",
                item_id_getter=operator.itemgetter(1),
                items="user_list",
                on_click=on_click,
            ),
        ),
        id='scroll_p',
        width=1,
        height=6,
        hide_on_single_page=True,
    ),
    SwitchTo(text=Const('🔙 назад'), state=AdminSG.menu, id='back'),
    state=AdminSG.set_privileges,
    getter=getter,
)
