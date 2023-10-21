from datetime import datetime, timedelta

import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.role import RoleFilter
from app.keyboards.reply.admin import main_kb
from app.models.role import UserRole
from app.settings import Settings
from app.states import KPIAnalytics, PublishSubscription
from app.texts import T

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
            print(f"[ERROR]: API respond with error: {request['error']}")
            raise ValueError
        return request
    except Exception as e:
        print(f"[ERROR]: API unable to respond due to: {e}")
        return None


@router.message(F.text == main_kb.BUTTON_REVOKE_OLD)
async def start_revoke_subscription(message: Message) -> None:
    await message.answer("...", reply_markup=main_kb.get())


@router.message(F.text == main_kb.BUTTON_KPI_ANALYTICS)
async def start_kpi_analytics(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_kpi"])

    await state.set_state(KPIAnalytics.days)


def _format_kpi_chunk(element: dict) -> str:
    return T["kpi_chunk"].format(
        element["all"],
        element["valid"],
        element["active"],
        element["expired"],
        element["revoked"],
    )


@router.message(StateFilter(KPIAnalytics.days))
async def finish_kpi_analytics(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    try:
        days = int(data.get("days"))
        if days <= 0:
            raise ValueError
    except ValueError:
        await message.answer(T["invalid_number"])
        return
    request = _api_call("analytics/kpi", {"period": days})
    if request is None:
        await message.answer(T["api_error"])
        return

    period_kpi = request["kpi"]["for_period"]
    period_chunks = "\n".join(
        [
            T["kpi_period_header"].format(
                (datetime.now() - timedelta(days=abs(int(key)))).strftime("%d/%m/%Y")
            )
            + _format_kpi_chunk(
                {
                    "revoked": period_kpi["revoked"][key],
                    "active": period_kpi["active"][key],
                    "valid": period_kpi["valid"][key],
                    "expired": period_kpi["expired"][key],
                    "all": period_kpi["all"][key],
                }
            )
            for key in dict(request["kpi"]["for_period"]["all"]).keys()
        ]
    )
    await message.answer(
        T["kpi_base"].format(
            _format_kpi_chunk(request["kpi"]["for_total"]),
            request["period"],
            period_chunks,
        )
    )
    await state.clear()


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
    request = _api_call("subscription/publish", {"days": days})
    if request is None:
        await message.answer(T["api_error"])
        return
    await message.answer(str(request))
    await state.clear()
