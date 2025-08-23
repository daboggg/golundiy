from aiogram_dialog import DialogManager

from bot.send_message import send_message
from parsers.anekdot_ru import get_random_phrase


def add_task(manager: DialogManager):
    variant = manager.dialog_data.get('selected_variant')
    times = manager.start_data.get('times')
    apscheduler = manager.middleware_data.get('apscheduler')
    user_id = manager.event.from_user.id

    if variant == 'афоризм':
        for time in times:
            time_lst = time.split(':')
            apscheduler.add_job(send_message,
                                trigger='cron',
                                hour=int(time_lst[0]),
                                minute=int(time_lst[1]),
                                kwargs={
                                    'user_id': user_id,
                                    'func': get_random_phrase
                                })
