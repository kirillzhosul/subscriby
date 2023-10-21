from json import dumps

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.role import RoleFilter
from app.keyboards.reply.admin import main_kb
from app.models.role import UserRole
from app.services.api import api_call
from app.states import PublishSubscription, RevokeSubscription
from app.texts import T

router = Router(name=__name__)
# Apply RoleFilter to all router's handlers
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


@router.message(F.text == main_kb.BUTTON_REVOKE_OLD)
async def start_revoke_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_key_to_revoke"])
    await state.set_state(RevokeSubscription.key)


@router.message(F.text == main_kb.BUTTON_CREATE_NEW)
async def start_publish_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_publish"])
    await state.set_state(PublishSubscription.days)


@router.message(StateFilter(RevokeSubscription.key))
async def finish_revoke_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(key=message.text)
    data = await state.get_data()
    key = str(data.get("key"))
    request = api_call("subscription/revoke", {"secret_key": key})
    if request is None:
        await message.answer(T["api_error"])
        return
    await state.clear()


@router.message(StateFilter(PublishSubscription.days))
async def finish_publish_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    try:
        days = int(data.get("days"))
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer(T["invalid_number"])
        return

    creator = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else f"{message.from_user.id}"
    )
    request = api_call(
        "subscription/publish",
        {
            "days": days,
            "payload": dumps(
                {
                    "version": 2,
                    "price": 0,
                    "source": f"Telegram [{creator}]",
                }
            ),
        },
    )
    if request is None:
        await message.answer(T["api_error"])
        return
    await state.clear()
