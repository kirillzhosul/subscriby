import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.role import RoleFilter
from app.keyboards.reply.admin import main_kb
from app.models.role import UserRole
from app.settings import Settings
from app.states import PublishSubscription

router = Router(name=__name__)
# Apply RoleFilter to all router's handlers
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


def _api_call(method: str, params: dict) -> dict | None:
    """
    Calls API and returns JSON response or None if error.
    """
    try:
        method_url = f"{Settings().subscriby_api_url}/{method}"
        request = requests.get(url=method_url, params=params).json()
        if "error" in request:
            raise ValueError
        return request
    except Exception as _:
        return None


@router.message(F.text == main_kb.BUTTON_REVOKE_OLD)
async def start_revoke_subscription(message: Message) -> None:
    await message.answer(
        "Revoking is not implemented yet...", reply_markup=main_kb.get()
    )


@router.message(F.text == main_kb.BUTTON_CREATE_NEW)
async def start_publish_subscription(message: Message, state: FSMContext) -> None:
    await message.answer("Please enter days for subscription (how long it will work)")
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
        await message.answer("Invalid days amount!")
        return
    request = _api_call("subscription/publish", {"days": days})
    if request is None:
        await message.answer("Unable to call API!")
        return
    await message.answer(str(request))
    await state.clear()
