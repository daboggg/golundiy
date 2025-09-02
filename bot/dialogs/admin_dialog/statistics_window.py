from collections import Counter

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, SwitchTo
from aiogram_dialog.widgets.text import Format, Const
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import AdminSG
from database.database import count_users, count_subscriptions, count_active_users, total_received_messages, \
    get_last_registered_user


async def getter(dialog_manager: DialogManager, **kwargs):
    # user_id = dialog_manager.event.from_user.id
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('apscheduler')
    all_jobs: list[Job] = apscheduler.get_jobs()
    # user_jobs: list[Job] = [job for job in all_jobs if job.name == str(user_id)]

    users_count: int = await count_users()
    users_active: int = await count_active_users()
    users_inactive: int = users_count - users_active

    # counter = Counter(getattr(job, 'name') for job in all_jobs)
    count_variants: Counter = Counter([job.kwargs.get('variant') for job in all_jobs])
    count_variants_msg: str = '     Подписок на:\n'
    for variant, quantity in count_variants.items():
        count_variants_msg += f'{variant}: {quantity}\n'

    last_registered_user = await get_last_registered_user()

    # print(await get_user(1117010300))
    # result =[]
    # for user_id, count in counter.items():
    #     user = await get_user(user_id)
    #     name = user[2] if not user[3] else f'{user[2]} {user[3]}'
    #     result.append((user_id, name, count))
    # print(result)

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


# async def on_user_selected(callback: CallbackQuery, button: Button,
#                               manager: DialogManager) -> None:
#     if button.widget_id == 'statistics':
#         await manager.switch_to(AdminSG.statistics)


statistics_window = Window(
    Format(Bold("Всего пользователей: {count_users}").as_html()),
    Format(Bold("Всего подписок: {count_subscribers}").as_html()),
    Format(Bold("Отправлено сообщений: {total_received_messages}").as_html()),
    Format(Bold("Активных пользователей: {users_active}").as_html()),
    Format(Bold("Неактивных пользователей: {users_inactive}").as_html()),
    Format(Bold("{count_variants_msg}").as_html()),
    Format(Bold("Последний зарегистрировавшийся пользователь:\n {last_registered_user}").as_html()),
    SwitchTo(text=Const('🔙 назад'), state=AdminSG.menu, id='back'),
    # ScrollingGroup(
    #         Select(
    #             Format("{item[1]}: {item[2]}"),
    #             id="users",
    #             item_id_getter=operator.itemgetter(0),
    #             items="users",
    #             on_click=on_user_selected,
    #         ),
    #         id='scroll',
    #         width=1,
    #         height=6,
    #         hide_on_single_page=True,
    #     ),
    state=AdminSG.statistics,
    getter=getter
)
