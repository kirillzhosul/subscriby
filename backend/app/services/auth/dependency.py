"""
    FastAPI dependency for auth
"""

from fastapi import Depends, Request
from starlette.exceptions import HTTPException

from app.plugins.custom_auth import CustomAuthPlugin
from app.settings import Settings, get_settings


def _get_secret_from_request(request: Request) -> str:
    """
    Returns secret from the request to pass auth check
    """
    secret = request.query_params.get("secret", request.headers.get("authorizaton", ""))
    return secret.removeprefix("Bearer ")


def _is_authorized(
    request: Request, method: str, secret_current: str, secret_required: str
) -> bool:
    match method:
        case "none":
            return True  # No authorization -> no checks
        case "secret":
            # -> User required to send secret key
            return secret_current == secret_required
        case "custom":
            # -> Custom user authorization with custom plugin class.
            return CustomAuthPlugin()(secret_key=secret_current, request=request)


def auth_required(request: Request, settings: Settings = Depends(get_settings)) -> None:
    """
    Checks authorization based on configuration
    """

    if not _is_authorized(
        request=request,
        method=settings.auth.method,
        secret_required=settings.auth.secret_key,
        secret_current=_get_secret_from_request(request=request),
    ):
        raise HTTPException(status_code=401)
