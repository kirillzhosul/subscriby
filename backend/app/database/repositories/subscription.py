from secrets import token_urlsafe
from datetime import timedelta, datetime

from sqlalchemy.orm import Session
from app.database.models.subscription import Subscription

from .base import SQLRepository


class SubscriptionRepository(SQLRepository):
    """
    Repository to deal with Subscription.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(db, Subscription)

    def create(self, days: int, payload="{}") -> Subscription:
        """
        Create, commit and return new subscription.
        """
        # Model fields
        expires_at = datetime.now() + timedelta(days=days)
        secret_key = token_urlsafe(24)

        # Commit
        subscription = Subscription(
            secret_key=secret_key, expires_at=expires_at, payload=payload
        )
        self.db.add(subscription)
        self.db.commit()
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

    def revoke(self, secret_key: str) -> None:
        """
        Revokes subscription by it secret key and returns None (if not found) or subscription.
        """
        if model := self.get(secret_key=secret_key):
            model.is_active = False
            self.db.add(model)
            self.db.commit()
            return model
