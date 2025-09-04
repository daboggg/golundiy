from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Row, Button, Back, SwitchTo, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.send_message import send_message
from bot.state_groups import MainSG
from database.database import is_privileged_user
from parsers.anekdot_ru import get_random_content


async def getter(dialog_manager: DialogManager, **kwargs):
    variant = dialog_manager.dialog_data.get('selected_variant')
    content = await get_random_content(variant)

    if variant in ['карикатуру', 'мем']:
        caption = content.get('caption')
        ct = ContentType.PHOTO if content.get('type') == 'image' else ContentType.VIDEO
        media = MediaAttachment(type=ct, url=content.get('src'))

        return {
            'media': media,
            'caption': caption,
        }

    else:
        return {
            'text': content
        }
    # {'src': 'https://www.anekdot.ru/i/caricatures/normal/20/3/2/1583153077.jpg', 'caption': 'Мем, Andrews',
    #  'type': 'image'}


async def on_again_selected(callback: CallbackQuery, button: Button,
                            manager: DialogManager) -> None:
    if button.widget_id == 'now':
        print(button.widget_id)
    else:
        manager.dialog_data["selected_period"] = int(button.widget_id)
        await manager.switch_to(MainSG.get_time)


get_now_window = Window(
    DynamicMedia("media", when='media'),
    Format(Bold("{caption}").as_html(), when='caption'),
    Format(Bold("{text}").as_html(), when='text'),
    SwitchTo(id='again', text=Const("Получить еще"), state=MainSG.get_now),
    Start(id='start', state=MainSG.get_variant, text=Const('Хватит'), mode=StartMode.RESET_STACK),
    # Row(
    #     Button(id='1', text=Const("1️⃣ раз в день"), on_click=on_period_selected),
    #     Button(id='2', text=Const("2️⃣ раза в день"), on_click=on_period_selected),
    # ),
    # Back(text=Const('🔙 назад')),
    state=MainSG.get_now,
    getter=getter,
)
