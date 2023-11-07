from json import dumps

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.reply.admin import main_kb
from app.roles import RoleFilter, UserRole
from app.services.api import api_call
from app.settings import TelegramSettings
from app.states import (
    InfoSubscription,
    PublishSubscription,
    RenewSubscription,
    RevokeSubscription,
)
from app.texts import T

router = Router(name=__name__)
# Apply RoleFilter to all router's handlers
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


@router.message(F.text == main_kb.BUTTON_RENEW_OLD)
async def start_renew_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_publish"], reply_markup=main_kb.get())
    await state.set_state(RenewSubscription.days)


@router.message(StateFilter(RenewSubscription.days))
async def renew_subscription_days(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    try:
        days = int(data.get("days"))
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer(T["invalid_number"], reply_markup=main_kb.get())
        await state.clear()
        return
    await message.answer(T["enter_key_to_renew"], reply_markup=main_kb.get())
    await state.set_state(RenewSubscription.key)


@router.message(StateFilter(RenewSubscription.key))
async def finish_renew_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(key=message.text)
    data = await state.get_data()
    key = str(data.get("key"))
    renew_type = "replace"
    request = await api_call(
        "subscription/renew",
        {"secret_key": key, "days": int(data.get("days")), "renew_type": renew_type},
    )
    if request is None:
        await message.answer(T["api_error"], reply_markup=main_kb.get())
        return
    if not TelegramSettings().expect_webhook_command_result:
        p = request["subscription"]
        await message.answer(
            T["subscription_renewed"].format(
                p["secret_key"], p["payload"], int(data.get("days")), renew_type
            ),
            reply_markup=main_kb.get(),
        )
    await state.clear()


@router.message(F.text == main_kb.BUTTON_REVOKE_OLD)
async def start_revoke_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_key_to_revoke"], reply_markup=main_kb.get())
    await state.set_state(RevokeSubscription.key)


@router.message(StateFilter(RevokeSubscription.key))
async def finish_revoke_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(key=message.text)
    data = await state.get_data()
    key = str(data.get("key"))
    request = await api_call("subscription/revoke", {"secret_key": key})
    if request is None:
        await message.answer(T["api_error"], reply_markup=main_kb.get())
        return
    if not TelegramSettings().expect_webhook_command_result:
        p = request["subscription"]
        await message.answer(
            T["subscription_revoked"].format(p["secret_key"], p["payload"]),
            reply_markup=main_kb.get(),
        )
    await state.clear()


@router.message(F.text == main_kb.BUTTON_KEY_INFO)
async def start_get_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_key_for_info"], reply_markup=main_kb.get())
    await state.set_state(InfoSubscription.key)


@router.message(StateFilter(InfoSubscription.key))
async def start_get_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(key=message.text)
    data = await state.get_data()
    key = str(data.get("key"))
    request = await api_call("subscription/check", {"secret_key": key})
    if request is None:
        await message.answer(T["api_error"], reply_markup=main_kb.get())
        return
    await message.answer(
        str(request),
        reply_markup=main_kb.get(),
    )
    await state.clear()


@router.message(F.text == main_kb.BUTTON_CREATE_NEW)
async def start_publish_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_publish"], reply_markup=main_kb.get())
    await state.set_state(PublishSubscription.days)


@router.message(StateFilter(PublishSubscription.days))
async def publish_subscription_days(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    try:
        days = int(data.get("days"))
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer(T["invalid_number"], reply_markup=main_kb.get())
        await state.clear()
        return
    await message.answer(T["enter_price_for_publish"], reply_markup=main_kb.get())
    await state.set_state(PublishSubscription.price)


@router.message(StateFilter(PublishSubscription.price))
async def finish_publish_subscription(message: Message, state: FSMContext) -> None:
    await state.update_data(price=message.text)
    data = await state.get_data()
    days = int(data.get("days"))
    try:
        price = int(data.get("price"))
        if price < 0:
            raise ValueError
    except ValueError:
        await message.answer(T["invalid_number"], reply_markup=main_kb.get())
        await state.clear()
        return

    creator = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else f"{message.from_user.id}"
    )
    request = await api_call(
        "subscription/publish",
        {
            "days": days,
            "payload": dumps(
                {
                    "version": 2,
                    "price": price,
                    "source": f"Telegram [{creator}]",
                }
            ),
        },
    )
    if request is None:
        await message.answer(T["api_error"], reply_markup=main_kb.get())
        return
    if not TelegramSettings().expect_webhook_command_result:
        p = request["subscription"]
        await message.answer(
            T["subscription_created"].format(
                p["secret_key"], p["expires_date"], p["payload"]
            ),
            reply_markup=main_kb.get(),
        )
    await state.clear()
