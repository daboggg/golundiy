from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choice_period() -> InlineKeyboardMarkup:

    ikb = InlineKeyboardBuilder()

    ikb.button(text=f'⏰ Установить', callback_data='ффф')
    ikb.button(text=f'✔️ Выполнено', callback_data='ыыы')

    return ikb.adjust(3).as_markup()
