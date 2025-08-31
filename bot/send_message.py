from typing import Any

from bot.core import bot
from bot.utils import format_content
from database.database import increase_counter_received_messages
from parsers.anekdot_ru import get_random_content


async def send_message(variant: str ,user_id: int) -> None:
    result: str|dict = await get_random_content(variant)
    title = format_content(variant)

    if variant in ['карикатуру', 'мем']:
        await bot.send_message(user_id, title)
        if result.get('type') == 'image':
            await bot.send_photo(user_id,photo=result.get('src'), caption=result.get('caption'))
        else:
            await bot.send_video(user_id, video=result.get('src'), caption=result.get('caption'))
    else:
        await bot.send_message(user_id, title + result)
    await increase_counter_received_messages(user_id)