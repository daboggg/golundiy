from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Start
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.state_groups import MainSG
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

async def on_again_selected(callback: CallbackQuery, button: Button,
                            manager: DialogManager) -> None:
    if button.widget_id == 'now':
        pass
    else:
        manager.dialog_data["selected_period"] = int(button.widget_id)
        await manager.switch_to(MainSG.get_time)


get_now_window = Window(
    DynamicMedia("media", when='media'),
    Format(Bold("{caption}").as_html(), when='caption'),
    Format(Bold("{text}").as_html(), when='text'),
    SwitchTo(id='again', text=Const("Получить еще"), state=MainSG.get_now),
    Start(id='start', state=MainSG.get_variant, text=Const('Хватит'), mode=StartMode.RESET_STACK),
    state=MainSG.get_now,
    getter=getter,
)
