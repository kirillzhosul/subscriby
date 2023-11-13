"""
    Service to deal with auth system
"""

from fastapi import Request
from starlette.exceptions import HTTPException

from app.plugins.custom_auth import CustomAuthPlugin
from app.settings import get_settings


class AuthDependency:
    """
    Checks authorization based on configuration
    """

    def _get_secret_from_request(self, req: Request) -> str:
        secret = req.query_params.get("secret", req.headers.get("authorizaton", ""))
        return secret.removeprefix("Bearer ")

    def __call__(self, req: Request) -> bool:
        match get_settings().auth.method:
            case "none":
                pass  # No authorization -> no checks
            case "secret":
                # -> User required to send secret key
                required_secret = get_settings().auth.secret_key
                if self._get_secret_from_request(req) != required_secret:
                    raise HTTPException(status_code=401)
                return True
            case "custom":
                # -> Custom user authorization with custom plugin class.
                plugin = CustomAuthPlugin()
                if plugin(secret_key=self._get_secret_from_request(req), request=req):
                    return True
                raise HTTPException(status_code=401)
        return False
