"""
    Router for subscription methods
"""

from secrets import token_urlsafe
from datetime import timedelta, datetime

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from app.services import AuthDependency
from app.serializers import serialize_subscription
from app.database.models import Subscription
from app.database.core import get_db

router = APIRouter(prefix="/subscription")


@router.get("/check")
def check(secret_key: str, db: Session = Depends(get_db)):
    if subscription := (
        db.query(Subscription).filter(Subscription.secret_key == secret_key).first()
    ):
        return serialize_subscription(subscription)
    return {"error": "Not Found"}


@router.get("/revoke", dependencies=[Depends(AuthDependency())])
def revoke(secret_key: str, db: Session = Depends(get_db)):
    if subscription := (
        db.query(Subscription).filter(Subscription.secret_key == secret_key).first()
    ):
        subscription.is_active = False
        db.add(subscription)
        db.commit()
        return serialize_subscription(subscription)
    return {"error": "Not Found"}


@router.get("/publish", dependencies=[Depends(AuthDependency())])
def publish(days: int = 3, db: Session = Depends(get_db)):
    expires_at = datetime.now() + timedelta(days=days)
    secret_key = token_urlsafe(24)
    subscription = Subscription(
        secret_key=secret_key, expires_at=expires_at, payload="{}"
    )
    db.add(subscription)
    db.commit()
    return serialize_subscription(subscription) | {"days": days}
