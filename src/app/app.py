from secrets import token_urlsafe
from datetime import timedelta, datetime

from starlette.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import Request, FastAPI, Depends, APIRouter

from .settings import Settings
from .serializers import serialize_subscription
from .database.models import Subscription
from .database.core import get_db, create_all

router = APIRouter(prefix="/subscription")


def auth_dependency(req: Request):
    match Settings().subscriby_auth_method:
        case "none":
            pass
        case "secret":
            if req.query_params.get("secret") != Settings().subscriby_auth_secret:
                raise HTTPException(status_code=401)


@router.get("/check")
def check(secret_key: str, db: Session = Depends(get_db)):
    if subscription := (
        db.query(Subscription).filter(Subscription.secret_key == secret_key).first()
    ):
        return serialize_subscription(subscription)
    return {"error": "Not Found"}


@router.get("/revoke", dependencies=[Depends(auth_dependency)])
def revoke(secret_key: str, db: Session = Depends(get_db)):
    if subscription := (
        db.query(Subscription).filter(Subscription.secret_key == secret_key).first()
    ):
        subscription.is_active = False
        db.add(subscription)
        db.commit()
        return serialize_subscription(subscription)
    return {"error": "Not Found"}


@router.get("/publish", dependencies=[Depends(auth_dependency)])
def publish(days: int = 3, db: Session = Depends(get_db)):
    expires_at = datetime.now() + timedelta(days=days)
    secret_key = token_urlsafe(24)
    subscription = Subscription(
        secret_key=secret_key, expires_at=expires_at, payload="{}"
    )
    db.add(subscription)
    db.commit()
    return serialize_subscription(subscription) | {"days": days}


def create_application():
    app = FastAPI()
    app.include_router(router)
    app.add_event_handler("startup", create_all)
    return app
