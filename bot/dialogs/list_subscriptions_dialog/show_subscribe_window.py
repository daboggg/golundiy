from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Format, Const
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import ListSubscriptionsSG


async def getter(dialog_manager: DialogManager, **kwargs):
    job_id = dialog_manager.dialog_data.get("job_id")
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
    job = apscheduler.get_job(job_id)

    variant: str = job.kwargs.get('variant')
    hour = job.next_run_time.hour
    minute = job.next_run_time.minute if job.next_run_time.minute > 9 else f'0{job.next_run_time.minute}'

    return {"subscribe_info": f'{variant} в {hour}:{minute}'}

async def on_delete_selected(callback: CallbackQuery, button: Button,
                             dialog_manager: DialogManager) -> None:
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
    apscheduler.remove_job(dialog_manager.dialog_data.get("job_id"))
    await callback.answer("подписка удалена")
    del dialog_manager.dialog_data["job_id"]
    await dialog_manager.switch_to(ListSubscriptionsSG.get_subscriptions)


show_subscribe_window = Window(
    Const('Каждый день вы получите'),
    Format('{subscribe_info}'),
    Back(Const("Назад")),
    Button(Const("Удалить"), id='delete_reminder', on_click=on_delete_selected),
    state=ListSubscriptionsSG.show_subscription,
    getter=getter
)
