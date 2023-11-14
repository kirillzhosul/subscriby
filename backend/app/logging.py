"""
    Logging system
"""

import logging
import sys

from .settings.logging import LoggingSettings


def init_logging() -> None:
    """
    Initialises logging configuration and more
    """
    settings = LoggingSettings()
    logging.basicConfig(
        format=settings.format,
        level=logging.getLevelName(settings.level.upper()),
        stream=sys.stdout,
    )
    loggers = [logging.getLogger("gunicorn.error"), logging.getLogger("uvicorn.error")]
    for logger in loggers:
        for handler in logger.handlers:
            handler.formatter = logging.Formatter(
                "[%(name)s] %(levelname)s: %(message)s"
            )


init_logging()
