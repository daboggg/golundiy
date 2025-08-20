from bot.core import bot


async def send_message(msg: str):
    print(msg)
    await bot.send_message(1117010300, msg)