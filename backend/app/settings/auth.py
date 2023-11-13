"""
    Auth system settings of the application
"""


from enum import Enum

from pydantic_settings import BaseSettings


class _AuthMethod(str, Enum):
    secret = "secret"
    none = "none"
    custom = "custom"


class AuthSettings(BaseSettings):
    """
    Environment auth settings
    """

    class Config:
        env_prefix = "AUTH_"

    # Auth method to handle
    method: _AuthMethod = _AuthMethod.none

    # Whatever secret word / key that used by `secret` auth method
    # or in your custom auth method
    secret_key: str = ""
