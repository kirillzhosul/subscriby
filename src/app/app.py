from secrets import token_urlsafe
from datetime import timedelta, datetime

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, APIRouter

from .serializers import serialize_subscription
from .database.models import Subscription
from .database.core import get_db, create_all

router = APIRouter(prefix="/subscription")


@router.get("/check")
def check(secret_key: str, db: Session = Depends(get_db)):
    if subscription := (
        db.query(Subscription).filter(Subscription.secret_key == secret_key).first()
    ):
        return serialize_subscription(subscription)
    return {"error": "Not Found"}


@router.get("/publish")
def publish(days: int = 3, db: Session = Depends(get_db)):
    expires_at = datetime.now() + timedelta(days=days)
    secret_key = token_urlsafe(24)
    subscription = Subscription(secret_key=secret_key, expires_at=expires_at)
    db.add(subscription)
    db.commit()
    return serialize_subscription(subscription) | {"days": days}


def create_application():
    app = FastAPI()
    app.include_router(router)
    app.add_event_handler("startup", create_all)
    return app
