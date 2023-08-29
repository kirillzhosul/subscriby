"""
`Subscriby` core model for subscription
"""

from sqlalchemy.sql import text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import String, Integer, DateTime, Column, Boolean

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

    # When subscription will expire
    expires_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
