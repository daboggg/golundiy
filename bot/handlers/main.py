import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.handlers.cmd import start_cmd

logger = logging.getLogger(__name__)

main = Router()

@main.message(F.text == 'Старт')
async def start_redirect(message:Message, dialog_manager: DialogManager):
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    await start_cmd(message, dialog_manager)