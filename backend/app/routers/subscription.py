"""
    Router for subscription methods
"""

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.database.core import get_repository
from app.database.repositories.subscription import SubscriptionRepository
from app.serializers.subscription import serialize_subscription
from app.services.auth import auth_required
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


@router.get("/revoke", dependencies=[Depends(auth_required)])
async def revoke(
    secret_key: str,
    background_tasks: BackgroundTasks,
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Revoke given subscription by secret
    """
    raw_subscription = repo.revoke(secret_key=secret_key)
    subscription = serialize_subscription(raw_subscription)
    if raw_subscription:
        background_tasks.add_task(
            broadcast_webhook_event, "subscription.revoke", subscription
        )
    return subscription


@router.get("/publish", dependencies=[Depends(auth_required)])
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


@router.get("/active", dependencies=[Depends(auth_required)])
def get_active(
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Get list of all active subscriptions
    """

    return {
        "subscriptions": [
            serialize_subscription(subscription, for_list=True)
            for subscription in repo.list_active()
        ]
    }


@router.get("/renew", dependencies=[Depends(auth_required)])
async def renew(
    secret_key: str,
    days: int,
    background_tasks: BackgroundTasks,
    renew_type: str = "replace",
    repo: SubscriptionRepository = Depends(get_repository(SubscriptionRepository)),
):
    """
    Renews given subscriptions via setting days left to given
    """
    if renew_type not in ("replace", "add"):
        raise HTTPException(status_code=400)

    raw_subscription = repo.renew(
        secret_key=secret_key, days=days, renew_type=renew_type
    )
    subscription = serialize_subscription(raw_subscription) | {
        "days": days,
        "renew_type": renew_type,
    }

    if raw_subscription:
        background_tasks.add_task(
            broadcast_webhook_event, "subscription.renew", subscription
        )
    return subscription
