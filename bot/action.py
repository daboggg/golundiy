from aiogram_dialog import DialogManager

from bot.send_message import send_message
from parsers.anekdot_ru import get_random_content


def add_task(manager: DialogManager):
    variant = manager.dialog_data.get('selected_variant')
    times = manager.start_data.get('times')
    apscheduler = manager.middleware_data.get('apscheduler')
    user_id = manager.event.from_user.id

    for time in times:
        time_lst = time.split(':')
        apscheduler.add_job(send_message,
                            trigger='cron',
                            hour=int(time_lst[0]),
                            minute=int(time_lst[1]),
                            kwargs={
                                'variant': variant,
                                'user_id': user_id,
                            })
