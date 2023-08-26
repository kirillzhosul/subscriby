from sqlalchemy.sql import text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import String, Integer, DateTime, Column, Boolean

from app.database.core import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    secret_key = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    payload = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))

    expires_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
