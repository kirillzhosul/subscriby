import time
from datetime import datetime

from app.database.models import Subscription


def serialize_subscription(subscription: Subscription) -> dict:
    return {
        "subscription": {
            "secret_key": subscription.secret_key,
            "expires_at": time.mktime(subscription.expires_at.timetuple()),
            "is_valid": datetime.now() > subscription.expires_at,
        }
    }
