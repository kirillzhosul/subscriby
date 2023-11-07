"""
    Main `Subscriby` FastAPI application
"""

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger

from .database.core import create_all
from .logger import logger
from .routers import analytics, subscription
from .services.webhook import notify_startup_with_webhook


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
    app.add_event_handler("startup", notify_startup_with_webhook)

    # Logging trick for `Gunicorn`
    fastapi_logger.handlers = logger.handlers
    logger.info("Applicated created!")

    return app
