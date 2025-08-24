import asyncio
import random

from aiogram.client.session import aiohttp
from bs4 import BeautifulSoup



urls = {
'фразу': 'https://www.anekdot.ru/random/aphorism/',
'анекдот': 'https://www.anekdot.ru/random/anekdot/',
'историю': 'https://www.anekdot.ru/random/story/',
'стишок': 'https://www.anekdot.ru/random/poems/',
}


async def get_random_content(variant:str)->str:
    async with aiohttp.ClientSession() as session:
        async with session.get(urls.get(variant)) as response:
            status = response.status
            text = await response.text()
    if status == 200:
        soup = BeautifulSoup(text, 'lxml')
        texts = soup.find_all('div', attrs={'class': 'text'})
        if variant == 'стишок':

            return ''.join([str(item) for item in random.choice(texts).contents]).replace('<br/>','\n')

        phrases = [item.text for item in texts]
        return random.choice(phrases)
    else:
        return 'что то пошло не так'

if __name__ == '__main__':
    asyncio.run(get_random_content('историю'))