"""
    Main FastAPI application
"""

from fastapi import FastAPI

from .handlers import add_handlers
from .logging import init_logging
from .routers import include_routers


def create_application() -> FastAPI:
    """
    Should be called inside Docker, returns application for `Gunicorn`
    """
    app = FastAPI()

    include_routers(app)
    add_handlers(app)
    init_logging()

    return app
