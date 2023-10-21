from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.role import RoleFilter
from app.keyboards.reply.admin import main_kb
from app.models.role import UserRole
from app.services.api import api_call
from app.states import PublishSubscription
from app.texts import T

router = Router(name=__name__)
# Apply RoleFilter to all router's handlers
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


@router.message(F.text == main_kb.BUTTON_REVOKE_OLD)
async def start_revoke_subscription(message: Message) -> None:
    await message.answer("...", reply_markup=main_kb.get())


@router.message(F.text == main_kb.BUTTON_CREATE_NEW)
async def start_publish_subscription(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_publish"])
    await state.set_state(PublishSubscription.days)


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
    request = api_call("subscription/publish", {"days": days})
    if request is None:
        await message.answer(T["api_error"])
        return

    subscription = request["subscription"]
    await message.answer(
        T["subscription_created"].format(
            subscription["secret_key"],
            subscription["expires_date"],
            subscription["payload"],
        )
    )
    await state.clear()
