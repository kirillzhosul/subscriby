"""
    Webhook system that is used for notifying configured targets about events
    TODO: Refactor with fallback stored system
"""
import time

from .sender import send_webhook_event
from app.settings import get_logger, get_settings


async def broadcast_webhook_event(name: str, payload: dict) -> None:
    """
    Tries to emit given webhook event to all configured targets
    """

    targets = get_settings().webhook.targets
    get_logger().info(
        f"[webhooks] Broadcasting event {name} to {len(targets)} targets..."
    )

    event = {
        "event": {
            "name": name,
            "payload": payload,
            "at": time.time(),
        }
    }

    for target in targets:
        await send_webhook_event(target, event)
