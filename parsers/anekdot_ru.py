import asyncio
import random

from aiogram.client.session import aiohttp
from bs4 import BeautifulSoup, Tag

urls = {
    'фразу': 'https://www.anekdot.ru/random/aphorism/',
    'анекдот': 'https://www.anekdot.ru/random/anekdot/',
    'историю': 'https://www.anekdot.ru/random/story/',
    'стишок': 'https://www.anekdot.ru/random/poems/',
    'карикатуру': 'https://www.anekdot.ru/random/caricatures/',
    'мем': 'https://www.anekdot.ru/random/mem/',
}


async def get_random_content(variant: str) -> str | dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(urls.get(variant)) as response:
            status = response.status
            text = await response.text()
    if status == 200:
        soup = BeautifulSoup(text, 'lxml')
        items = soup.find_all('div', attrs={'class': 'text'})

        if variant in ['карикатуру', 'мем']:
            item: Tag = random.choice(items)
            while True:
                try:
                    return {
                        'src': item.find('img').attrs['src'],
                        'caption': item.find('img').attrs['alt'],
                        'type': 'image',
                    }
                except AttributeError:
                    try:
                        return {
                            'src': item.find('source').attrs['src'],
                            'caption': item.find('div').attrs['title'],
                            'type': 'video',
                        }
                    except AttributeError:
                        continue

        if variant in ['стишок', 'историю']:
            return ''.join([str(item) for item in random.choice(items).contents]).replace('<br/>', '\n')

        phrases = [item.text for item in items]
        return random.choice(phrases)
    else:
        raise ConnectionError
        # return 'что то пошло не так'


if __name__ == '__main__':
    asyncio.run(get_random_content('историю'))
