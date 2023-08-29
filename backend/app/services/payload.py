"""
    Payload processing service.
"""
from app.plugins.custom_payload import CustomPayloadPlugin


def preprocess_payload(payload: str) -> str:
    """
    Preprocesses payload via parsing and formatting back or raises error
    """
    plugin = CustomPayloadPlugin()
    return plugin(payload=payload)
