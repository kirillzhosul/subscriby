"""
    Base classes for plugins
"""
from abc import ABC, abstractmethod

from fastapi import Request
from pydantic import BaseModel

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


class BaseModelPayload(BaseModel):
    """
    Base injected
    """

    # Version of the application
    # used for your own needs to detect subscription is legacy/should be noticed
    version: int = 1

    # Source of the subscription
    # for you, there will be information like, telegram frontend as the source or
    # your own place where you publish subscription
    source: str = "backend.unset"

    # Price of the subscription
    # Left 0 if you do not receive revenue from your subscriptions
    price: int = 0


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
