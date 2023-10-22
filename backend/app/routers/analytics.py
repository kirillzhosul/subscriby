"""
    Router for KPI (analytics, statistics) methods
"""

from datetime import datetime, timedelta
from statistics import mean

from fastapi import APIRouter, Depends

from app.database.core import get_repository
from app.database.repositories.subscription import SubscriptionRepository
from app.plugins.custom_kpi import CustomKPIPlugin
from app.services.auth import AuthDependency
from app.settings import Settings

router = APIRouter(prefix="/analytics")


@router.get("/kpi/total", dependencies=[Depends(AuthDependency())])
def get_kpi_for_total(
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Returns KPI analytics for whole time
    """

    plugin = CustomKPIPlugin()
    counters = repo.get_total_kpi_counters()
    percents = {
        "revoked": round(counters["revoked"] / counters["all"] * 100, 2),
        "expired": round(counters["expired"] / counters["all"] * 100, 2),
        "valid": round(counters["valid"] / counters["all"] * 100, 2),
    }
    return {
        "kpi": {
            "counters": counters,
            "percents": percents,
        }
        | plugin.extend_kpi(repo),
    }


@router.get("/kpi/period", dependencies=[Depends(AuthDependency())])
def get_kpi_for_period(
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
    days: int = 7,
):
    """
    Returns KPI analytics for period in days
    """

    plugin = CustomKPIPlugin()
    counters = repo.get_period_kpi_counters(days)

    periods = {
        k: (
            {v: counters[v][k] for v in counters.keys()}
            | {
                "date": (datetime.now() - timedelta(days=abs(k))).strftime(
                    Settings().date_format
                )
            }
        )
        for k in counters["all"].keys()
    }
    percents = {"published_average": round(mean(counters["all"].values()), 2)}
    return {
        "period_days": days,
        "kpi": {"periods": periods, "percents": percents}
        | plugin.extend_kpi_for_period(days, repo),
    }
