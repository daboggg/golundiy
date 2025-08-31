from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Const, Format

from bot.state_groups import MainSG
from bot.utils import check_time_format


async def getter(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    period = dialog_manager.dialog_data.get('selected_period')
    if period == 1:
        return {'msg': f'✏️ Пожалуйста введите ⏱️время в формате чч:мм'}
    else:
        if dialog_manager.start_data.get('count') == 0:
            return {'msg': f'✏️Пожалуйста введите первое ⏱️время в формате чч:мм'}
        else:
            return {'msg': f'✏️ Пожалуйста введите второе ⏱️время в формате чч:мм'}

async def success(message: Message,
                  text_input: TextInput,
                  manager: DialogManager,
                  text:str):
    manager.start_data['count'] += 1
    manager.start_data['times'].append(text)
    if manager.dialog_data.get('selected_period') == 1:
        await manager.next()
    else:
        if manager.start_data.get('count') > 1:
            await manager.next()



async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer(Bold("НЕПРАВИЛЬНЫЙ ФОРМАТ ВРЕМЕНИ!").as_html())

async def back(
        callback: CallbackQuery,
        widget: Any,
        manager: DialogManager,
):
    manager.start_data.get('times').clear()


get_time_window = Window(
    Format(Bold("{msg}").as_html()),
    Back(text=Const('🔙 назад'), on_click=back),
    TextInput(id='time', on_error=error, on_success=success, type_factory=check_time_format),
    state=MainSG.get_time,
    getter=getter,
)
