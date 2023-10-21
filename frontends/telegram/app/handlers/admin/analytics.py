from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.role import RoleFilter
from app.keyboards.reply.admin import main_kb
from app.models.role import UserRole
from app.services.api import api_call
from app.states import KPIAnalytics
from app.texts import T

router = Router(name=__name__)
# Apply RoleFilter to all router's handlers
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


def _format_kpi_chunk(e: dict) -> str:
    return T["kpi_chunk"].format(
        e["all"],
        e["valid"],
        e["active"],
        e["expired"],
        e["revoked"],
    )


@router.message(F.text == main_kb.BUTTON_KPI_ANALYTICS)
async def start_kpi_analytics(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_kpi"])
    await state.set_state(KPIAnalytics.days)


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
    request = api_call("analytics/kpi", {"period": days})
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
            for key in dict(request["kpi"]["for_period"]["all"])
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
