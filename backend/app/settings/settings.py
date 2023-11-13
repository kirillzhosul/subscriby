"""
    Core settings holder with all other settings dependants
"""

from functools import lru_cache

from pydantic_settings import BaseSettings

from .auth import AuthSettings
from .database import DatabaseSettings
from .logging import LoggingSettings
from .webhook import WebhookSettings


class Settings(BaseSettings):
    """
    All of the application settings from environment
    """

    database: DatabaseSettings = DatabaseSettings()
    webhook: WebhookSettings = WebhookSettings()
    auth: AuthSettings = AuthSettings()
    logging: LoggingSettings = LoggingSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns single instance of the settings
    """
    return Settings()
