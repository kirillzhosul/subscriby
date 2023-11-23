"""
    Subscription serializer
"""

import time
from datetime import datetime

import pytz

from app.database.models import Subscription
from app.services.payload import parse_payload


def serialize_subscription(
    subscription: Subscription | None = None, for_list: bool = False
) -> dict:
    """
    Serializes subscription into dict or error if none.
    """
    if not isinstance(subscription, Subscription):
        return {"error": "Subscription with given ID not found"}
    expires_date = None
    expires_at = None
    is_valid = subscription.is_active
    if subscription.expires_at:
        expires_at: datetime = subscription.expires_at.replace(tzinfo=pytz.UTC)
        expires_date = expires_at.strftime("%Y.%m.%d")
        is_valid &= datetime.now().replace(tzinfo=pytz.UTC) < expires_at
        expires_at: float = time.mktime(expires_at.timetuple())

    data = {
        "secret_key": subscription.secret_key,
        "expires_at": expires_at,
        "expires_date": expires_date,
        "payload": parse_payload(subscription.payload),
        "is_valid": is_valid,
    }

    return data if for_list else {"subscription": data}
