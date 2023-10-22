"""
    Repository to deal with subscriptions
"""
from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import Callable

from sqlalchemy import Integer, func, or_
from sqlalchemy.orm import Query, Session

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

    def get_count_for_period(
        self, days: int, *, _ext_filter: Callable[[Query], Query] | None = None
    ) -> dict[int, int]:
        """
        Returns count of subscriptions created within each day within period in days
        """
        if not _ext_filter:
            _ext_filter = lambda query: query

        today = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        delta = timedelta(days=days)
        items = {-i: 0 for i in range(days)}
        for i, v in enumerate(
            _ext_filter(
                self.db.query(
                    func.date(Subscription.created_at),
                    func.count(Subscription.id),
                )
                .group_by(func.date(Subscription.created_at))
                .filter(Subscription.created_at >= today - delta)
                .filter(Subscription.created_at <= today + timedelta(days=1))
            ).all()
        ):
            items[-i] = v[1]
        return items

    def get_revenue_for_period(self, days: int) -> dict[int, int]:
        """
        Returns revenue within each day for period in days
        """

        today = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        delta = timedelta(days=days)
        items = {-i: 0 for i in range(days)}
        for i, v in enumerate(
            self.db.query(
                func.date(Subscription.created_at),
                func.sum(func.cast(Subscription.payload["price"], Integer)),
            )
            .group_by(func.date(Subscription.created_at))
            .filter(Subscription.created_at >= today - delta)
            .filter(Subscription.created_at <= today + timedelta(days=1))
            .all()
        ):
            items[-i] = v[1] or 0
        return items

    def get_total_revenue(self) -> int:
        """
        Returns total revenue by calculating price
        """
        return self.db.query(
            func.sum(func.cast(Subscription.payload["price"], Integer))
        ).first()[0]

    def get_revoked_for_period(self, days: int) -> dict[int, int]:
        """
        Returns revoked count of subscriptions created within each day within period in days
        """
        return self.get_count_for_period(
            days=days,
            _ext_filter=lambda query: query.filter(not Subscription.is_active),
        )

    def get_active_for_period(self, days: int) -> dict[int, int]:
        """
        Returns active count of subscriptions created within each day within period in days
        """
        return self.get_count_for_period(
            days=days, _ext_filter=lambda query: query.filter(Subscription.is_active)
        )

    def get_valid_for_period(self, days: int) -> dict[int, int]:
        # sourcery skip: none-compare
        """
        Returns valid count of subscriptions created within each day within period in days
        """
        return self.get_count_for_period(
            days=days,
            _ext_filter=lambda query: query.filter(Subscription.is_active).filter(
                or_(
                    Subscription.expires_at > datetime.now(),
                    Subscription.expires_at == None,
                )
            ),
        )

    def get_expired_for_period(self, days: int) -> dict[int, int]:
        """
        Returns expired count of subscriptions created within each day within period in days
        """
        return self.get_count_for_period(
            days=days,
            _ext_filter=lambda query: query.filter(
                Subscription.expires_at <= datetime.now()
            ),
        )

    def get_revoked_count(self) -> int:
        """
        Get count for all revoked subscriptions
        """
        return self.db.query(Subscription).filter(not Subscription.is_active).count()

    def get_expired_count(self) -> int:
        """
        Get count for all expired subscriptions
        """
        return (
            self.db.query(Subscription)
            .filter(Subscription.expires_at <= datetime.now())
            .count()
        )

    def get_active_count(self) -> int:
        """
        Get count for all active subscriptions
        """
        return self.db.query(Subscription).filter(Subscription.is_active).count()

    def get_valid_count(self) -> int:
        """
        Get count for all valid subscriptions
        """
        return (
            self.db.query(Subscription)
            .filter(Subscription.is_active)
            .filter(
                or_(
                    Subscription.expires_at > datetime.now(),
                    Subscription.expires_at == None,
                )
            )
            .count()
        )

    def get_total_kpi_counters(self) -> dict:
        """
        Returns dict for KPI counters for whole time
        """
        return {
            "all": self.get_count(),
            "valid": self.get_valid_count(),
            "revoked": self.get_revoked_count(),
            "expired": self.get_expired_count(),
            "active": self.get_active_count(),
            "revenue": self.get_total_revenue(),
        }

    def get_period_kpi_counters(self, days: int) -> dict:
        """
        Returns dict for KPI counters for period in days
        """
        return {
            "all": self.get_count_for_period(days),
            "valid": self.get_valid_for_period(days),
            "revoked": self.get_revoked_for_period(days),
            "expired": self.get_expired_for_period(days),
            "active": self.get_active_for_period(days),
            "revenue": self.get_revenue_for_period(days),
        }

    def get_count(self) -> int:
        """
        Get count for all subscriptions
        """
        return self.db.query(Subscription).count()
