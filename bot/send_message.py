from typing import Any

from bot.core import bot


async def send_message(user_id: int, func: Any) -> None:
    res = await func()
    await bot.send_message(user_id, res)