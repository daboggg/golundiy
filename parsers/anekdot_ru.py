import asyncio
import random

from aiogram.client.session import aiohttp
from bs4 import BeautifulSoup

URL = 'https://www.anekdot.ru/random/aphorism/'


async def get_random_phrase():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            status = response.status
            text = await response.text()
    if status == 200:
        soup = BeautifulSoup(text, 'lxml')
        phrases = [item.text for item in soup.find_all('div', attrs={'class': 'text'})]
        return random.choice(phrases)
    else:
        return 'что то пошло не так'

if __name__ == '__main__':
    asyncio.run(get_random_phrase())