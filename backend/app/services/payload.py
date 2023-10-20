"""
    Payload processing service
"""
from json import loads

from app.plugins.custom_payload import CustomPayloadPlugin


def preprocess_payload(payload: str) -> str:
    """
    Preprocesses payload via parsing and formatting back or raises error
    """
    plugin = CustomPayloadPlugin()
    return str(plugin(payload=payload))


def parse_payload(payload: str) -> dict:
    """
    Parses payload and returns dict out of that
    """
    return loads(payload)
