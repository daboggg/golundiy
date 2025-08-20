from typing import Any

from bot.core import bot


async def send_message(msg: str, func: Any) -> None:
    res = await func()
    print(msg)
    await bot.send_message(1117010300, res)