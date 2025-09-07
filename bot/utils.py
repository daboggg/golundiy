import re

from aiogram.utils.formatting import Bold
from aiogram_dialog import DialogManager
from apscheduler.job import Job

from database.database import get_user, is_privileged_user
from settings import settings


def check_time_format(time: str) -> str:
    if not re.match('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time):
        raise ValueError()

    return time


def set_time_message(
        selected_variant: str,
        selected_period: int,
        times: list[str]
) -> str:
    period = '1️⃣ раз в день.\n' if selected_period == 1 else '2️⃣ раза в день.\n'
    time = f'В {digit_to_emoji(times[0])}.' if len(
        times) == 1 else f'В {digit_to_emoji(times[0])} и в {digit_to_emoji(times[1])}.'

    if selected_variant == 'фразу':
        return f'✔️Выбрана фраза {period}{time}'
    if selected_variant == 'анекдот':
        return f'✔️Выбран анекдот {period}{time}'
    if selected_variant == 'историю':
        return f'✔️Выбрана история {period}{time}'
    if selected_variant == 'стишок':
        return f'✔️Выбран стишок {period}{time}'
    if selected_variant == 'карикатуру':
        return f'✔️Выбрана карикатура {period}{time}'
    if selected_variant == 'мем':
        return f'✔️Выбран мем {period}{time}'


variants = {
    'анекдот': 'анекдот',
    'историю': 'история',
    'фразу': 'фраза',
    'стишок': 'стишок',
    'карикатуру': 'карикатура',
    'мем': 'мем',
}


def format_content(variant: str) -> str:
    return Bold(f'Вот вам {variants[variant]}:\n\n').as_html()


def digit_to_emoji(time: str) -> str:
    digits_lst = {
        0: '0️⃣',
        1: '1️⃣',
        2: '2️⃣',
        3: '3️⃣',
        4: '4️⃣',
        5: '5️⃣',
        6: '6️⃣',
        7: '7️⃣',
        8: '8️⃣',
        9: '9️⃣',
    }
    res = ''
    for item in time:
        if item.isdigit():
            res += digits_lst[int(item)]
        else:
            res += item
    return res


async def check_max_subscribe(dialog_manager: DialogManager) -> bool:
    user_id = dialog_manager.event.from_user.id
    if user_id == settings.bots.admin_id:
        return False

    count_user_jobs = await get_count_user_jobs(dialog_manager)
    is_privileged =  await is_privileged_user(user_id)

    if is_privileged:
        if count_user_jobs >= settings.custom.subscription_privileged_limit:
            return count_user_jobs
    else:
        if count_user_jobs >= settings.custom.subscription_limit:
            return count_user_jobs
    return False


async def get_count_user_jobs(dialog_manager):
    user_id = dialog_manager.event.from_user.id
    apscheduler = dialog_manager.middleware_data.get('apscheduler')
    all_jobs: list[Job] = apscheduler.get_jobs()
    user_jobs: list[Job] = [job for job in all_jobs if job.name == str(user_id)]
    return len(user_jobs)
