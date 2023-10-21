import time

import requests

from app.logger import logger
from app.settings import Settings


def emit_webhook_event(event_name: str, event_payload: dict) -> None:
    payload = {
        "event_name": event_name,
        "event_payload": event_payload,
        "event_at": time.time(),
    }
    targets = Settings().subscriby_webhook_targets
    logger.info(
        f"Emmitting webhoook with event name {event_name} to {len(targets)} targets!"
    )
    for target in targets:
        try:
            requests.post(target, json=payload, timeout=5)
        except requests.RequestException as e:
            logger.error(f"Webhook target error: {e}")
    logger.info("Emmitting webhoook finished!")
