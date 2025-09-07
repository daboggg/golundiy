from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Row, Button, Group, Start
from aiogram_dialog.widgets.text import Const, Format

from bot.state_groups import MainSG, AdminSG, ListSubscriptionsSG
from bot.utils import check_max_subscribe
from database.database import is_privileged_user
from settings import settings


async def getter(dialog_manager: DialogManager, **kwargs):
    is_admin = settings.bots.admin_id == dialog_manager.event.from_user.id
    is_max_subscribe = await check_max_subscribe(dialog_manager)
    if is_max_subscribe:
        if await is_privileged_user(dialog_manager.event.from_user.id):
            limit = settings.custom.subscription_privileged_limit
        else:
            limit = settings.custom.subscription_limit
        limit_msg: str = (f'Вы достигли лимита ({is_max_subscribe}/{limit})'
                          if limit == is_max_subscribe
                          else f'Вы превысили лимит ({is_max_subscribe}/{limit})')

    else:
        limit_msg = ''

    return {
        'is_admin': is_admin,
        'is_max_subscribe': is_max_subscribe,
        'show_buttons': not is_max_subscribe,
        'limit_msg': limit_msg,
    }


async def on_variant_selected(callback: CallbackQuery, button: Button,
                              manager: DialogManager) -> None:
    if button.widget_id == 'admin':
        await manager.start(AdminSG.menu, mode=StartMode.RESET_STACK)
    else:
        manager.dialog_data["selected_variant"] = await button.text.render_text(manager.dialog_data, manager)
        await manager.switch_to(MainSG.get_period)


variant_window = Window(
    Const(Bold("❓ Что вам послать?").as_html(), when='show_buttons'),
    Format(Bold("{limit_msg}").as_html(), when='is_max_subscribe'),
    Const(Bold("Чтобы создать новую подписку, можете удалить ненужную").as_html(), when='is_max_subscribe'),
    Group(
        Row(
            Button(id='admin', text=Const('💼 admin'), when='is_admin', on_click=on_variant_selected),
        ),
        Row(
            Button(id='anecdote', text=Const("анекдот"), on_click=on_variant_selected),
            Button(id='phrase', text=Const("фразу"), on_click=on_variant_selected),

        ),
        Row(
            Button(id='story', text=Const("историю"), on_click=on_variant_selected),
            Button(id='poem', text=Const("стишок"), on_click=on_variant_selected),
        ),
        Row(
            Button(id='caricature', text=Const("карикатуру"), on_click=on_variant_selected),
            Button(id='mem', text=Const("мем"), on_click=on_variant_selected),
        ),
        when='show_buttons'
    ),
    Start(id='to_list_subscribers', text=Const('список подписок'), state=ListSubscriptionsSG.get_subscriptions,
          mode=StartMode.RESET_STACK, when='is_max_subscribe'),
    state=MainSG.get_variant,
    getter=getter
)
