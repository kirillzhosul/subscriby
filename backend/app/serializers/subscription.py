"""
    Subscription serializer.
"""

import time
from datetime import datetime

import pytz
from app.settings import Settings
from app.services.payload import parse_payload
from app.database.models import Subscription


def serialize_subscription(subscription: Subscription | None = None) -> dict:
    """
    Serializes subscription into dict or error if none.
    """
    if not isinstance(subscription, Subscription):
        return {"error": "Subscription with given ID not found"}
    expires_at = subscription.expires_at.replace(tzinfo=pytz.UTC)
    expires_date = expires_at.strftime(Settings().subscriby_expires_date_format)
    is_valid = (
        datetime.now().replace(tzinfo=pytz.UTC) < expires_at and subscription.is_active
    )

    return {
        "subscription": {
            "secret_key": subscription.secret_key,
            "expires_at": time.mktime(expires_at.timetuple()),
            "expires_date": expires_date,
            "payload": parse_payload(subscription.payload),
            "is_valid": is_valid,
        }
    }
