"""
    Service to deal with auth system.
"""
from starlette.exceptions import HTTPException
from fastapi import Request

from app.settings import Settings


class AuthDependency:
    """
    Checks authorization based on configuration.
    """

    def __call__(self, req: Request) -> bool:
        match Settings().subscriby_auth_method:
            case "none":
                pass  # No authorization -> no checks
            case "secret":
                # -> User required to send secret key
                secret = req.query_params.get("secret", "")
                required_secret = Settings().subscriby_auth_secret
                if secret != required_secret:
                    raise HTTPException(status_code=401)
                return True
        return False
