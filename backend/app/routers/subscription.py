"""
    Router for subscription methods
"""

from fastapi import APIRouter, BackgroundTasks, Depends

from app.database.core import get_repository
from app.database.repositories.subscription import SubscriptionRepository
from app.serializers.subscription import serialize_subscription
from app.services.auth import AuthDependency
from app.services.payload import preprocess_payload
from app.services.webhook import broadcast_webhook_event

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
async def revoke(
    secret_key: str,
    background_tasks: BackgroundTasks,
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Revoke given subscription by secret
    """
    subscription = serialize_subscription(repo.revoke(secret_key=secret_key))
    background_tasks.add_task(
        broadcast_webhook_event, "subscription.revoke", subscription
    )
    return subscription


@router.get("/publish", dependencies=[Depends(AuthDependency())])
async def publish(
    background_tasks: BackgroundTasks,
    days: int | None = 3,
    payload: str = "{}",
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Create new subscription for given days and payload
    """
    subscription = serialize_subscription(
        repo.create(days=days, payload=preprocess_payload(payload=payload))
    ) | {"days": days}

    background_tasks.add_task(
        broadcast_webhook_event, "subscription.publish", subscription
    )
    return subscription
