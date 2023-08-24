from sqlalchemy.sql import func
from sqlalchemy import String, Integer, DateTime, Column
from app.database.core import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    secret_key = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
