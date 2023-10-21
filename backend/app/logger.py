"""
    Logging configuration
"""
from logging import getLogger

DEFAULT_WSGI_LOGGER_NAME = "gunicorn.error"

logger = getLogger(DEFAULT_WSGI_LOGGER_NAME)
