import asyncio
import logging

import aiosqlite
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

# from bot.comands import set_commands
from bot.core import bot, scheduler
from bot.dialogs.main_dialog.main_dialog import main_dialog
# from bot.dialogs.list_reminders_dialog import list_reminders_dialog
# from bot.dialogs.main_dialog import main_dialog
from bot.handlers.cmd import cmd_router
# from bot.handlers.done_reminder import done_reminder_router
# from bot.handlers.other import other_router
from bot.middlewares.apschedmiddleware import SchedulerMiddleware
from settings import settings


async def start_bot(bot: Bot):
    pass
    # async with aiosqlite.connect(settings.db.db_name) as db:
    #     await db.execute('''
    #         CREATE TABLE IF NOT EXISTS users (
    #             id INTEGER PRIMARY KEY,
    #             user_id INTEGER NOT NULL,
    #             firstname TEXT,
    #             lastnave TEXT,
    #             email TEXT
    #         )
    #     ''')
    # await set_commands(bot)
    # await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    pass
    # await bot.send_message(settings.bots.admin_id, text='Бот остановлен')
    # scheduler.shutdown()


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger(__name__)

    # запускаю скедулер
    scheduler.start()

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # регистрация middlewares
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    # подключение роутеров
    dp.include_routers(
        cmd_router,
        main_dialog,
        # done_reminder_router,
        # main_dialog,
        # list_reminders_dialog,
        # other_router
    )

    # подключение диалогов
    setup_dialogs(dp)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    logger.info('start')

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
