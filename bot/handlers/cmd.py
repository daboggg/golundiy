from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.state_groups import MainSG, ListSubscriptionsSG
from database.database import create_user

cmd_router = Router()


# отрабатывает по команде /start
@cmd_router.message(CommandStart())
async def start_cmd(message:Message, dialog_manager: DialogManager) -> None:
    print(message)
    await create_user(message)

    kb = [
        [types.KeyboardButton(text="Старт")],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("⛵️⛵️⛵️⛵️⛵", reply_markup=keyboard)

    await dialog_manager.start(MainSG.get_variant, mode=StartMode.RESET_STACK, data={'count': 0, 'times': []})


# # отрабатывает по команде /list, отображает список напоминаний
@cmd_router.message(Command(commands="list"))
async def list_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ListSubscriptionsSG.get_subscriptions, mode=StartMode.RESET_STACK)
