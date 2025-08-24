from typing import Any

from bot.core import bot
from bot.utils import format_content
from parsers.anekdot_ru import get_random_content


async def send_message(variant: str ,user_id: int) -> None:
    result = await get_random_content(variant)
    msg = format_content(result, variant)
    await bot.send_message(user_id, msg)