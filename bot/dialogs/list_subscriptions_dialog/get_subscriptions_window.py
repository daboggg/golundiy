import operator
import datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Row, Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Case
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import MainSG, ListSubscriptionsSG
from bot.utils import variants



async def getter(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    all_jobs: list[Job] = apscheduler.get_jobs()

    user_jobs: list[Job] = [job for job in all_jobs if job.name == str(user_id)]
    result = list()
    for job in user_jobs:
        variant: str = variants.get(job.kwargs.get('variant'))
        hour = job.next_run_time.hour

        minute = job.next_run_time.minute if job.next_run_time.minute > 9 else f'0{job.next_run_time.minute}'

        result.append((datetime.time(hour=int(hour), minute=int(minute)), f'{variant} в {hour}:{minute}', job.id))
    return {
        'subscribers': sorted(result, key=operator.itemgetter(0)),
        "count": str(len(user_jobs)),
    }


async def on_subscribe_selected(callback: CallbackQuery, widget: Any,
                                manager: DialogManager, item_id: str):
    manager.dialog_data['job_id'] = item_id
    await manager.next()


get_subscriptions_window = Window(
    Const(Bold("📋Список ваших подписок").as_html()),
    Case(
        {
            "0": Const("            🫲   🫱"),
            ...: Format("           всего: {count} 👇")
        },
        selector="count"
    ),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="subscribers",
            item_id_getter=operator.itemgetter(2),
            items="subscribers",
            on_click=on_subscribe_selected,
        ),
        id='scroll',
        width=1,
        height=6,
        hide_on_single_page=True,
    ),
    state=ListSubscriptionsSG.get_subscriptions,
    getter=getter
)
