"""
    Router for subscription methods
"""

from fastapi import Depends, APIRouter
from app.services import preprocess_payload, AuthDependency
from app.serializers import serialize_subscription
from app.plugins import CustomPayloadPlugin
from app.database.repositories.subscription import SubscriptionRepository
from app.database.core import get_repository

router = APIRouter(prefix="/subscription")


@router.get("/check")
def check(
    secret_key: str,
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Check that given subscription is exists and valid
    """
    return serialize_subscription(repo.get(secret_key=secret_key))


@router.get("/revoke", dependencies=[Depends(AuthDependency())])
def revoke(
    secret_key: str,
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Revoke given subscription by secret
    """
    return serialize_subscription(repo.revoke(secret_key=secret_key))


@router.get("/publish", dependencies=[Depends(AuthDependency())])
def publish(
    days: int = 3,
    payload: str = "{}",
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Create new subscription for given days and payload
    """
    if payload != "{}":
        payload = preprocess_payload(payload=payload)
        return {"error": "Payload injection is not implemented yet"}
    return serialize_subscription(repo.create(days=days, payload=payload)) | {
        "days": days
    }
