"""
    System for serializing stuff into response dict, should be models (Pydantic).
"""

from .subscription import serialize_subscription

__all__ = ["serialize_subscription"]
