"""
    Core sender of the webhook events
"""


import contextlib

from aiohttp import ClientResponse, ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from app.settings import get_settings


async def _handle_response(response: ClientResponse) -> bool:
    """
    Handles response from the target and validates them
    """
    # TODO: handle checks for HMAC and other
    return response.status == 200


async def _handle_request(session: ClientSession, target: str, payload: dict) -> bool:
    """
    Handles request and response after that
    """
    request_kwargs = {"allow_redirects": False, "json": payload}
    with contextlib.suppress(ClientError):
        async with session.post(url=target, **request_kwargs) as response:
            return await _handle_response(response)
    return False


async def send_webhook_event(target: str, payload: dict) -> bool:
    """
    Notifies single target about webhook event and returns OK/ERROR
    """

    async with ClientSession(
        timeout=ClientTimeout(total=get_settings().webhook.timeout)
    ) as session:
        return await _handle_request(session, target, payload)
