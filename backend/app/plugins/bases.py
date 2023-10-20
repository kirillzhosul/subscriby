"""
    Base classes for plugins
"""
from abc import ABC, abstractmethod

from fastapi import Request

from app.database.repositories.subscription import SubscriptionRepository


class BaseAuthPlugin(ABC):
    """
    Base plugin for auth check
    """

    @abstractmethod
    def __call__(self, secret_key: str, request: Request) -> bool:
        ...


class BasePayloadPlugin(ABC):
    """
    Base plugin for payload validation / parsing
    """

    @abstractmethod
    def __call__(self, payload: str) -> str:
        ...


class BaseKPIPlugin(ABC):
    """
    Base plugin for KPI analytics
    """

    @abstractmethod
    def extend_kpi_for_period(self, days: int, repo: SubscriptionRepository) -> dict:
        ...

    @abstractmethod
    def extend_kpi(self, repo: SubscriptionRepository) -> dict:
        ...
