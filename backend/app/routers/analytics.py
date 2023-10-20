"""
    Router for KPI (analytics, statistics) methods
"""

from fastapi import APIRouter, Depends

from app.database.core import get_repository
from app.database.repositories.subscription import SubscriptionRepository
from app.plugins import CustomKPIPlugin
from app.services import AuthDependency

router = APIRouter(prefix="/analytics")


@router.get("/kpi", dependencies=[Depends(AuthDependency())])
def get_kpi(
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
    period: int = 7,
):
    """
    Returns KPI analytics
    """

    plugin = CustomKPIPlugin()
    p_plugin = plugin.extend_kpi_for_period(period, repo)
    p_all = repo.get_count_for_period(period)
    p_revoked = repo.get_revoked_for_period(period)
    p_active = repo.get_active_for_period(period)
    p_valid = repo.get_valid_for_period(period)
    p_expired = repo.get_expired_for_period(period)

    t_plugin = plugin.extend_kpi(repo)
    t_revoked = repo.get_revoked_count()
    t_expired = repo.get_expired_count()
    t_active = repo.get_active_count()
    t_valid = repo.get_valid_count()
    t_all = repo.get_count()

    return {
        "period": period,
        "kpi": {
            "for_period": {
                "revoked": p_revoked,
                "active": p_active,
                "valid": p_valid,
                "expired": p_expired,
                "all": p_all,
            }
            | p_plugin,
            "for_total": {
                "revoked": t_revoked,
                "active": t_active,
                "valid": t_valid,
                "expired": t_expired,
                "all": t_all,
            }
            | t_plugin,
        },
    }
