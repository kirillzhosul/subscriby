from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.reply.admin import main_kb
from app.roles import RoleFilter, UserRole
from app.services.api import api_call
from app.settings import TelegramSettings
from app.states import KPIAnalytics
from app.texts import T

router = Router(name=__name__)
# Apply RoleFilter to all router's handlers
router.message.filter(RoleFilter(UserRole.ADMIN))
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


def _format_kpi_chunk(e: dict) -> str:
    return T["kpi_chunk"].format(
        f"{e['revenue'] or 0} {TelegramSettings().revenue_currency}",
        e["all"],
        e["valid"],
        e["active"],
        e["expired"],
        e["revoked"],
    )


@router.message(F.text == main_kb.BUTTON_KPI_ANALYTICS)
async def start_kpi_analytics(message: Message, state: FSMContext) -> None:
    await message.answer(T["enter_days_for_kpi"], reply_markup=main_kb.get())
    await state.set_state(KPIAnalytics.days)


@router.message(StateFilter(KPIAnalytics.days))
async def finish_kpi_analytics(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    try:
        days = int(data.get("days"))
        if days <= 1:
            raise ValueError
    except ValueError:
        await message.answer(T["invalid_number"], reply_markup=main_kb.get())
        return
    total_kpi = await api_call("analytics/kpi/total", {})
    if total_kpi is None:
        return await message.answer(T["api_error"], reply_markup=main_kb.get())
    period_kpi = await api_call("analytics/kpi/period", {"days": days})
    if period_kpi is None:
        return await message.answer(T["api_error"], reply_markup=main_kb.get())

    periods = dict(period_kpi["kpi"]["periods"])
    period_chunks = "\n".join(
        [
            T["kpi_period_header"].format(periods[key]["date"])
            + _format_kpi_chunk(
                {
                    "revoked": periods[key]["revoked"],
                    "active": periods[key]["active"],
                    "valid": periods[key]["valid"],
                    "expired": periods[key]["expired"],
                    "all": periods[key]["all"],
                    "revenue": periods[key]["revenue"],
                }
            )
            for key in periods
        ]
    )
    await message.answer(
        T["kpi_base"].format(
            total_kpi["kpi"]["percents"]["revoked"],
            total_kpi["kpi"]["percents"]["expired"],
            total_kpi["kpi"]["percents"]["valid"],
            _format_kpi_chunk(total_kpi["kpi"]["counters"]),
            period_kpi["period_days"],
            period_chunks,
            period_kpi["kpi"]["percents"]["published_average"],
        ),
        reply_markup=main_kb.get(),
    )
    await state.clear()
