"""
    Router for KPI (analytics, statistics) methods
"""

from statistics import mean

from fastapi import APIRouter, Depends, HTTPException

from app.database.core import get_repository
from app.database.repositories.subscription import SubscriptionKPIRepository
from app.plugins.custom_kpi import CustomKPIPlugin
from app.services.auth import auth_required

router = APIRouter(prefix="/analytics")


@router.get("/kpi/total", dependencies=[Depends(auth_required)])
def get_kpi_for_total(
    repo: SubscriptionKPIRepository = Depends(
        get_repository(SubscriptionKPIRepository)
    ),
    only_with_price: bool = False,
):
    """
    Returns KPI analytics for whole time
    """

    plugin = CustomKPIPlugin()
    counters = repo.get_counters(days=None, only_with_price=only_with_price)
    percents = {
        "revoked": round(counters["revoked"] / counters["all"] * 100, 2),
        "expired": round(counters["expired"] / counters["all"] * 100, 2),
        "valid": round(counters["valid"] / counters["all"] * 100, 2),
    }
    return {
        "only_with_price": only_with_price,
        "kpi": {
            "counters": counters,
            "percents": percents,
        }
        | plugin.extend_kpi(only_with_price, repo),
    }


@router.get("/kpi/period", dependencies=[Depends(auth_required)])
def get_kpi_for_period(
    repo: SubscriptionKPIRepository = Depends(
        get_repository(SubscriptionKPIRepository)
    ),
    only_with_price: bool = False,
    days: int = 7,
    periods_as_list: bool = False,
):
    """
    Returns KPI analytics for period in days
    """
    if days < 1:
        raise HTTPException(status_code=400)
    plugin = CustomKPIPlugin()
    counters = repo.get_counters(days=days, only_with_price=only_with_price)

    periods = {
        date: (
            {key: (counters[key].get(date, 0) or 0) for key in counters.keys()}
            | {"date": date.strftime("%Y.%m.%d")}
        )
        for date in counters["all"].keys()
    }
    if periods_as_list:
        periods = list(periods.values())

    percents = {"published_average": round(mean(counters["all"].values()), 2)}
    return {
        "period_days": days,
        "periods_as_list": periods_as_list,
        "only_with_price": only_with_price,
        "kpi": {"periods": periods, "percents": percents}
        | plugin.extend_kpi_for_period(days, only_with_price, repo),
    }
