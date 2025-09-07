from collections import Counter

from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import AdminSG
from database.database import count_users, count_subscriptions, count_active_users, total_received_messages, \
    get_last_registered_user


async def getter(dialog_manager: DialogManager, **kwargs):
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    all_jobs: list[Job] = apscheduler.get_jobs()

    users_count: int = await count_users()
    users_active: int = await count_active_users()
    users_inactive: int = users_count - users_active

    count_variants: Counter = Counter([job.kwargs.get('variant') for job in all_jobs])
    count_variants_msg: str = '     Подписок на:\n'
    for variant, quantity in count_variants.items():
        count_variants_msg += f'{variant}: {quantity}\n'

    last_registered_user = await get_last_registered_user()

    return {
        'count_users': users_count,
        'count_subscribers': await count_subscriptions(),
        'users_active': users_active,
        'users_inactive': users_inactive,
        'count_variants_msg': count_variants_msg,
        'total_received_messages': await total_received_messages(),
        'last_registered_user': last_registered_user[2] if not last_registered_user[
            3] else f'{last_registered_user[2]} {last_registered_user[3]}',
    }

statistics_window = Window(
    Format(Bold("✔️ Всего пользователей: {count_users}").as_html()),
    Format(Bold("✔️ Всего подписок: {count_subscribers}").as_html()),
    Format(Bold("✔️ Отправлено сообщений: {total_received_messages}").as_html()),
    Format(Bold("✔️ Активных пользователей: {users_active}").as_html()),
    Format(Bold("✔️ Неактивных пользователей: {users_inactive}").as_html()),
    Format(Bold("✔️ {count_variants_msg}").as_html()),
    Format(Bold("✔️ Последний зарегистрировавшийся пользователь:\n {last_registered_user}").as_html()),
    SwitchTo(text=Const('🔙 назад'), state=AdminSG.menu, id='back'),
    state=AdminSG.statistics,
    getter=getter
)
