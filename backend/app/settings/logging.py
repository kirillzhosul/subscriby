"""
    Logging system settings of the application
"""


from typing import Literal

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    """
    Environment logging settings
    """

    class Config:
        env_prefix = "LOGGING_"

    level: Literal[
        "debug", "notset", "info", "warn", "warning", "error", "fatal", "critical"
    ] = "debug"
    format: str = "[%(name)s] %(levelname)s: %(message)s"
