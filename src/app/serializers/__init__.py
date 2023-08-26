import time
from datetime import datetime

import pytz

from app.database.models import Subscription


def serialize_subscription(subscription: Subscription) -> dict:
    expires_at: datetime = subscription.expires_at.replace(tzinfo=pytz.UTC)
    return {
        "subscription": {
            "secret_key": subscription.secret_key,
            "expires_at": time.mktime(subscription.expires_at.timetuple()),
            "is_valid": datetime.now().replace(tzinfo=pytz.UTC) > expires_at,
        }
    }
