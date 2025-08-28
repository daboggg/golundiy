from datetime import datetime, timedelta

import aiosqlite
from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.keyboards.choice_period import choice_period
from bot.send_message import send_message
from bot.state_groups import MainSG, ListSubscriptionsSG
from database.database import create_user
from settings import settings

# from aiogram_dialog import DialogManager, StartMode

# from bot.state_groups import MainDialogSG, ListOfRemindersSG

cmd_router = Router()


# отрабатывает по команде /start
@cmd_router.message(CommandStart())
async def start_cmd(message:Message, dialog_manager: DialogManager) -> None:
    await create_user(message)
    await dialog_manager.start(MainSG.get_variant, mode=StartMode.RESET_STACK, data={'count': 0, 'times': []})



# @cmd_router.message(CommandStart())
# async def cmd_start(message: Message,bot: Bot, apscheduler: AsyncIOScheduler) -> None:

#     apscheduler.add_job(send_message,
#                         trigger='cron',
#                         # run_date=datetime.now() + timedelta(seconds=10),
#                         # hour=11,
#                         minute='*',
#                         kwargs={'msg': 'test_message'})
#     await message.answer('Выберите периодичность рассылки', reply_markup=choice_period())


# # отрабатывает по команде /start
# @cmd_router.message(CommandStart())
# async def cmd_start(message: Message, dialog_manager: DialogManager) -> None:
#     await dialog_manager.start(MainDialogSG.start, mode=StartMode.RESET_STACK)


# # отрабатывает по команде /list, отображает список напоминаний
@cmd_router.message(Command(commands="list"))
async def list_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ListSubscriptionsSG.get_subscriptions, mode=StartMode.RESET_STACK)


# # отрабатывает по команде /help
# @cmd_router.message(Command(commands="help"))
# async def list_reminders(message: Message) -> None:
#     await message.answer('⁉️ Чтобы начать, нажмите  меню -> /start')
