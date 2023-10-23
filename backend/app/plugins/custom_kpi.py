"""
    Custom plugin for KPI analytics
"""

from .bases import BaseKPIPlugin
from app.database.repositories.subscription import SubscriptionRepository


class CustomKPIPlugin(BaseKPIPlugin):
    """
    Custom plugin for KPI analytics
    """

    def extend_kpi_for_period(
        self, days: int, only_with_price: bool, repo: SubscriptionRepository
    ) -> dict:
        return {}

    def extend_kpi(self, only_with_price: bool, repo: SubscriptionRepository) -> dict:
        return {}
