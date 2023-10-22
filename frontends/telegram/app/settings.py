"""
    Environment settings
"""

from pydantic_settings import BaseSettings


class SubscribySettings(BaseSettings):
    """
    Environment settings for `Subscriby`
    """

    class Config:
        env_prefix = "SUBSCRIBY_"

    auth_method: str = "none"
    auth_secret: str | None = None  # For `secret` auth method.
    api_host: str
    hook_path: str


class TelegramSettings(BaseSettings):
    """
    Environment settings for Telegram
    """

    class Config:
        env_prefix = "TELEGRAM_"

    admin_ids: list[int]
    token: str
    language: str = "EN"
    revenue_currency: str
    web_host: str
    hook_path: str
    http_internal_port: int
    http_internal_host: str
    expect_webhook_command_result: bool = True
