"""
    Webhook system that is used for notifying configured targets about events
    TODO: Refactor with fallback stored system
"""
import time
from logging import getLogger

from .events import WebhookEventType
from .sender import send_webhook_event
from app.settings import get_settings

logger = getLogger("service.webhooks.broadcaster")


def _build_event(event_type: WebhookEventType, payload: dict) -> dict:
    """
    Builds event based on given data
    """
    event = {
        "name": event_type.value,
        "payload": payload,
        "at": time.time(),
    }
    return {"event": event}


async def broadcast_webhook_event(event_type: WebhookEventType, payload: dict) -> None:
    """
    Tries to emit given webhook event to all configured targets
    """
    if not get_settings().webhook.enabled:
        return
    targets = get_settings().webhook.targets
    logger.debug(f"Sending event '{event_type}' to {len(targets)} targets...")
    for target in targets:
        await send_webhook_event(target, _build_event(event_type, payload))
