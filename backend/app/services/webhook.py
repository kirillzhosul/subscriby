"""
    Webhook system that is used for notifying configured targets about events
    TODO: Refactor with fallback stored system
"""
import time

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from fastapi import BackgroundTasks

from app.logger import logger
from app.settings import Settings


async def _notify_webhook_target(target: str, payload: dict) -> None:
    """
    Notifies single target about event webhook
    """

    try:
        async with ClientSession() as session:
            async with session.post(target, json=payload, allow_redirects=False) as _:
                pass
    except ClientError as e:
        logger.warning(
            "[webhooks] One of the targets is unable to respond!", exc_info=e
        )


async def notify_startup_with_webhook() -> None:
    """
    Notifies webhook listeners for backend restarted / went online
    """
    BackgroundTasks().add_task(broadcast_webhook_event, "api.startup", {})


async def broadcast_webhook_event(name: str, payload: dict) -> None:
    """
    Tries to emit given webhook event to all configured targets
    """
    targets = Settings().webhook_targets
    logger.info(f"[webhooks] Broadcasting event {name} to {len(targets)} targets...")

    event = {
        "event": {
            "name": name,
            "payload": payload,
            "at": time.time(),
        }
    }
    for target in targets:
        await _notify_webhook_target(target, event)
