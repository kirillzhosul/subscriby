"""
    Custom plugin for checking auth
"""
from fastapi import Request

from .bases import BaseAuthPlugin


class CustomAuthPlugin(BaseAuthPlugin):
    """
    Custom plugin for checking auth
    """

    def __call__(self, secret_key: str, request: Request) -> bool:
        _ = secret_key
        _ = request
        return True
