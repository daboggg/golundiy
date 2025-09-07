import operator
from collections import Counter
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import AdminSG
from database.database import get_users


async def getter(dialog_manager: DialogManager, **kwargs):
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    all_jobs: list[Job] = apscheduler.get_jobs()
    counter = Counter(getattr(job, 'name') for job in all_jobs)
    all_users = await get_users()
    users_list = []

    for user in all_users:
        name = user[2] if not user[3] else f'{user[2]} {user[3]}'
        number = counter.get(str(user[1])) if counter.get(str(user[1])) else 0
        users_list.append((user[1], name, number))

    return {
        'users': users_list,
    }


async def on_user_selected(callback: CallbackQuery, widget: Any,
                                manager: DialogManager, item_id: str):
    manager.dialog_data['user_id'] = item_id
    await manager.switch_to(state=AdminSG.user_detail)


users_window = Window(
    Const("👥 Пользователи"),
    ScrollingGroup(
        Select(
            Format("👤 {item[1]}  {item[2]}"),
            id="users",
            item_id_getter=operator.itemgetter(0),
            items="users",
            on_click=on_user_selected,
        ),
        id='scroll',
        width=1,
        height=6,
        hide_on_single_page=True,
    ),
    SwitchTo(text=Const('🔙 назад'), state=AdminSG.menu, id='back'),
    state=AdminSG.users,
    getter=getter
)
