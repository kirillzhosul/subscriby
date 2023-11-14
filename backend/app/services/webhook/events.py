"""
    Events system with some sort of DTOs
"""
from enum import Enum


class WebhookEventType(str, Enum):
    """
    All types of the webhooks from the server
    """

    subscription_published = "subscription.publish"
    subscription_revoked = "subscription.revoke"
    subscription_renew = "subscription.renew"
    subscription_expired = "subscription.expired"  # TODO: not implemented
    server_startup = "server.startup"
    server_error = "server.error"  # TODO: not implemented
