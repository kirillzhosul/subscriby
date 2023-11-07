"""
    Repository to deal with subscriptions
"""
from datetime import date, datetime, timedelta
from functools import partial
from secrets import token_urlsafe
from typing import Any

from sqlalchemy import Integer, func, or_
from sqlalchemy.orm import Session

from .base import SQLRepository
from app.database.models.subscription import Subscription


class SubscriptionRepository(SQLRepository):
    """
    Repository to deal with Subscription
    """

    def __init__(self, db: Session) -> None:
        super().__init__(db, Subscription)

    def create(self, days: int, payload: dict = None) -> Subscription:
        """
        Create, commit and return new subscription
        """
        if payload is None:
            payload = {}

        expires_at = (datetime.now() + timedelta(days=days)) if days != 0 else None
        subscription = Subscription(
            secret_key=token_urlsafe(24),
            expires_at=expires_at,
            payload=payload,
        )
        self.add_and_commit(subscription)
        return subscription

    def get(self, secret_key: str) -> Subscription | None:
        """
        Returns one subscription by secret key or None if not found
        """
        return (
            self.db.query(Subscription)
            .filter(Subscription.secret_key == secret_key)
            .first()
        )

    def revoke(self, secret_key: str) -> Subscription | None:
        """
        Revokes subscription by it secret key and returns None (if not found) or subscription.
        """
        if model := self.get(secret_key=secret_key):
            model.is_active = False
            self.add_and_commit(model)
            return model

    def renew(
        self, secret_key: str, days: int, renew_type: str = "replace"
    ) -> Subscription | None:
        """
        Revokes subscription by it secret key and returns None (if not found) or subscription.
        """
        delta = timedelta(days=days)
        if model := self.get(secret_key=secret_key):
            if renew_type == "replace":
                model.expires_at = (datetime.now() + delta) if days != 0 else None
            elif renew_type == "add":
                model.expires_at += delta
            self.add_and_commit(model)
            return model


class SubscriptionKPIRepository(SubscriptionRepository):
    """
    Subscription repository with KPI/analytics methods
    """

    def _calculate_kpi_query_periodic(
        self,
        days: int,
        only_with_price: bool,
        query_row: Any,
        query_filters: list[Any] | None,
    ) -> dict[date, Any]:
        """
        Returns KPI query result for period as dict from period (-i) to result
        """
        # Current date for comparing under current date
        now = datetime.now()
        today = datetime(year=now.year, month=now.month, day=now.day)

        # Custom query
        query = (
            self.db.query(func.date(Subscription.created_at), query_row)
            .group_by(func.date(Subscription.created_at))
            .filter(Subscription.created_at >= today - timedelta(days=days))
            .filter(Subscription.created_at <= today + timedelta(days=1))
        )

        if only_with_price:
            query = query.filter(func.cast(Subscription.payload["price"], Integer) != 0)

        # Map custom filters
        if query_filters:
            query = query.filter(*query_filters)

        # Map query result
        return {row[0]: row[1] for row in query.all()}

    def get_count(
        self,
        days: int | None = None,
        only_with_price: bool = False,
        query_filters: list[Any] | None = None,
    ) -> dict[date, int] | int:
        """
        Returns count of subscriptions created within each day within period in days
        or total if days is not specified
        """
        if days is None:
            query = self.db.query(Subscription)
            if query_filters:
                query = query.filter(*query_filters)
            if only_with_price:
                query = query.filter(
                    func.cast(Subscription.payload["price"], Integer) != 0
                )
            return query.count()
        return self._calculate_kpi_query_periodic(
            days=days,
            only_with_price=only_with_price,
            query_row=func.count(Subscription.id),
            query_filters=query_filters,
        )

    def get_revenue(self, days: int | None = None) -> dict[date, int] | int:
        """
        Returns revenue within each day for period in days or for total
        if days is not specified
        """

        row = func.sum(func.cast(Subscription.payload["price"], Integer))
        if days is None:
            return self.db.query(row).first()[0]
        return self._calculate_kpi_query_periodic(
            days=days,
            only_with_price=False,  # Due to SUM already does not sums non-priced
            query_row=row,
            query_filters=[],
        )

    def get_counters(
        self, days: int | None, only_with_price: bool
    ) -> dict[str, dict[date, Any]]:
        # sourcery skip: none-compare
        """
        Returns dict for KPI counters for whole time or periodic if days is specified
        """
        get = partial(self.get_count, days, only_with_price)
        return {
            "all": get(),
            "revenue": self.get_revenue(days=days),
            "expired": get([Subscription.expires_at <= datetime.now()]),
            "revoked": get([Subscription.is_active == False]),
            "active": get([Subscription.is_active == True]),
            "valid": get(
                [
                    Subscription.is_active,
                    or_(
                        Subscription.expires_at > datetime.now(),
                        Subscription.expires_at == None,
                    ),
                ]
            ),
        }
