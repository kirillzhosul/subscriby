"""
    Environment settings for `Subscriby` Telegram
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Environment settings for `Subscriby` Telegram
    """

    subscriby_auth_method: str = "none"
    subscriby_auth_secret: str | None = None  # For `secret` auth method.
    subscriby_api_url: str
    subscriby_telegram_admin_ids: list[int]
    subscriby_telegram_token: str
    subscriby_telegram_language: str = "EN"
    subscriby_telegram_web_host: str
