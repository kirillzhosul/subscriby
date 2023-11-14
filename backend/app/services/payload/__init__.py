"""
    Injected payload business logic service
"""

from json import loads

from app.plugins.custom_payload import CustomPayloadPlugin


def preprocess_payload(payload: str) -> dict:
    """
    Preprocesses payload via parsing or returns default
    """
    plugin = CustomPayloadPlugin()
    return parse_payload(plugin(payload=payload))


def parse_payload(payload: str | dict) -> dict:
    """
    Parses payload and returns dict out of that
    """
    return payload if isinstance(payload, dict) else loads(payload)


__all__ = ["preprocess_payload", "parse_payload"]
