from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Format, Const
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import AdminSG
from bot.utils import digit_to_emoji
from database.database import get_user


async def getter(dialog_manager: DialogManager, **kwargs):
    user_id: str = dialog_manager.dialog_data.get('user_id')
    user: tuple = await get_user(int(user_id))
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    all_jobs: list[Job] = apscheduler.get_jobs()
    user_jobs: list[Job] = [job for job in all_jobs if job.name == str(user_id)]
    name: str = user[2] if not user[3] else f'{user[2]} {user[3]}'

    msg = '     Подписан на:\n' if user_jobs else '     Подписок нет'

    for uj in user_jobs:
        hour = uj.next_run_time.hour
        minute = uj.next_run_time.minute if uj.next_run_time.minute > 9 else f'0{uj.next_run_time.minute}'
        time: str = f'{hour}:{minute}'
        msg += f'🚩 {uj.kwargs.get("variant")} в {digit_to_emoji(time)}\n'

    return {
        'name': name,
        'msg': msg,
    }


async def on_user_selected(callback: CallbackQuery, widget: Any,
                           manager: DialogManager, item_id: str):
    manager.dialog_data['user_id'] = item_id
    await manager.switch_to()


user_detail_window = Window(
    Format("👤 {name}\n"),
    Format("{msg}\n"),
    Back(Const('🔙назад')),
    state=AdminSG.user_detail,
    getter=getter
)
