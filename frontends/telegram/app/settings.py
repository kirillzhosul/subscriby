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
    subscriby_api_url: str = "https://sunstrike-subscriby.florgon.com/"
    subscriby_telegram_admin_ids: list[int] = [1444462272, 5484667168]
    subscriby_telegram_token: str = "6470728017:AAF9Lai9ah6zxbHpfGwZcP37IaYFe2Dnniw"
