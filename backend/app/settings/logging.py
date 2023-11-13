"""
    Logging system settings of the application
"""


from functools import lru_cache
from logging import Logger, getLogger

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    """
    Environment logging settings
    """

    class Config:
        env_prefix = "LOGGING_"


@lru_cache(maxsize=1)
def get_logger() -> Logger:
    """
    Temporary solution.
    TODO: Resolve that
    https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19?ysclid=loxe26k59t67545868
    """
    return getLogger("gunicorn.error")
