"""
    `Subscriby` core model for subscription
"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func, text

from app.database.core import Base


class Subscription(Base):
    """
    `Subscriby` core model for subscription
    """

    __tablename__ = "subscriptions"

    # System
    id = Column(Integer, primary_key=True, index=True)

    # Subscription key / token for user.
    secret_key = Column(String, nullable=False, unique=True)

    # Can be false when admins revokes subscription
    is_active = Column(Boolean, default=True)

    # Injected payload inside subscription for external systems (websites and etc)
    payload = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))

    # Datetimes
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
