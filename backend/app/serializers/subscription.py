"""
    Subscription serializer.
"""

import time
from datetime import datetime

import pytz

from app.database.models import Subscription


def serialize_subscription(subscription: Subscription) -> dict:
    """
    Serializes subscription into dict.
    """
    expires_at = subscription.expires_at.replace(tzinfo=pytz.UTC)
    is_valid = (
        datetime.now().replace(tzinfo=pytz.UTC) < expires_at and subscription.is_active
    )
    return {
        "subscription": {
            "secret_key": subscription.secret_key,
            "expires_at": time.mktime(expires_at.timetuple()),
            "is_valid": is_valid,
        }
    }
