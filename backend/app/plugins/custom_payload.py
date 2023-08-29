"""
Custom plugin for payload validation / parsing
"""
from .bases import BasePayloadPlugin


class CustomPayloadPlugin(BasePayloadPlugin):
    """
    Custom plugin for payload validation / parsing
    """

    def __call__(self, payload: str) -> dict:
        _ = payload
        return {}
