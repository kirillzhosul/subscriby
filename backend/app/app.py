"""
    Main `Subscriby` FastAPI application
"""

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger

from .database.core import create_all
from .routers import analytics, subscription
from .settings import get_logger


def create_application() -> FastAPI:
    """
    Should be called inside Docker, returns application for `Gunicorn`
    """
    app = FastAPI()

    # Routers (TODO: Migrate inside)
    app.include_router(analytics.router)
    app.include_router(subscription.router)

    # Events
    app.add_event_handler("startup", create_all)

    # Logging trick for `Gunicorn`
    fastapi_logger.handlers = get_logger().handlers
    get_logger().info("Applicated created!")

    return app
