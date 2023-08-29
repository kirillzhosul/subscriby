import requests
from aiogram.types import Message
from aiogram.dispatcher import FSMContext, Dispatcher

from .states import PublishSubscription
from .settings import Settings
from .keyboards import main_menu, BUTTON_REVOKE_OLD, BUTTON_CREATE_NEW


async def _check_for_admin(message: Message) -> bool:
    """
    Returns user is admin or not and send message if not.
    ! TODO: Migrate with middlewares / another right solution.
    """
    admin_ids = Settings().subscriby_telegram_admin_ids
    is_admin = message.from_user.id in admin_ids
    if not is_admin:
        await message.answer("<b>Sorry, you are not an admin!</b>")
    return is_admin


def _api_call(method: str, params: dict) -> dict | None:
    """
    Calls API and returns JSON response or None if error.
    """
    try:
        method_url = Settings().subscriby_api_url + f"/{method}"
        request = requests.get(url=method_url, params=params).json()
        if "error" in request:
            raise ValueError
        return request
    except Exception as _:
        return None


async def start_command(message: Message) -> None:
    """
    Handler for `/start` command.
    """
    if not await _check_for_admin(message):
        return
    await message.answer(
        f"Welcome to <b>Subscriby</b>, <i>{message.from_user.full_name}</i>!",
        reply_markup=main_menu(),
    )


async def start_revoke_subscription(message: Message) -> None:
    await message.answer("Revoking is not implemented yet...")


async def start_publish_subscription(message: Message) -> None:
    await message.answer("Please enter days for subscription (how long it will work)")
    await PublishSubscription.days.set()


async def finish_publish_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    try:
        days = int(data.get("days"))
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Invalid days amount!")
        return
    request = _api_call("subscription/publish", {"days": days})
    if request is None:
        await message.answer("Unable to call API!")
        return
    await message.answer(str(request))
    await state.finish()


def register_handlers(dispatcher: Dispatcher) -> None:
    """
    Registers message handlers for dispatcher of the bot
    """
    dispatcher.register_message_handler(start_command, commands="start")
    dispatcher.register_message_handler(
        start_publish_subscription, text=BUTTON_CREATE_NEW
    )

    dispatcher.register_message_handler(
        finish_publish_subscription, PublishSubscription.days
    )
    dispatcher.register_message_handler(
        start_revoke_subscription, text=BUTTON_REVOKE_OLD
    )
