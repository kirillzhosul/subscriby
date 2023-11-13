"""
    Webhook system settings of the application
"""


from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class WebhookSettings(BaseSettings):
    """
    Environment webhooks settings
    """

    class Config:
        env_prefix = "WEBHOOK_"

    # Is webhooks enabled or not
    enabled: bool = True

    # List of event names that is excluded and not broadcasted
    excluded: list[str] = []

    # Timeout for waiting target accept response
    timeout: float = 15.0

    # TODO: maybe migrate that inside database model so it is configurable at the top level?
    # TODO: allow to separate event types for certain target
    # Declares HTTP targets of the webhooks
    targets: list[str] = []
