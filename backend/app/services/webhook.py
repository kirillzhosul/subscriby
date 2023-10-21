"""
    Webhook system that is used for notifying configured targets about events
    TODO: Refactor with fallback stored system
"""
import asyncio
import time

from aiohttp import request
from aiohttp.client_exceptions import ClientError

from app.logger import logger
from app.settings import Settings


async def _notify_webhook_target(target: str, payload: dict) -> None:
    """
    Notifies single target about event webhook
    """
    try:
        await request("POST", target, json=payload, allow_redirects=False)
    except ClientError as e:
        logger.warning(
            "[webhooks] One of the targets is unable to respond!", exc_info=e
        )


async def broadcast_webhook_event(name: str, payload: dict) -> None:
    """
    Tries to emit given webhook event to all configured targets
    """
    targets = Settings().subscriby_webhook_targets
    logger.info(f"[webhooks] Broadcasting event {name} to {len(targets)} targets...")

    event = {
        "event": {
            "name": name,
            "payload": payload,
            "at": time.time(),
        }
    }
    tasks = [
        asyncio.ensure_future(notify_webhook_target(target, event))
        for target in targets
    ]
    await asyncio.wait(tasks)
