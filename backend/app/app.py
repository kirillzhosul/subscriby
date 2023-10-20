"""
    FastAPI application
"""
from fastapi import FastAPI

from .database.core import create_all
from .routers.analytics import router as analytics_router
from .routers.subscription import router as subscription_router


def create_application() -> FastAPI:
    """
    Returns prepared and ready to run application
    """
    app = FastAPI()
    app.include_router(analytics_router)
    app.include_router(subscription_router)
    app.add_event_handler("startup", create_all)
    return app
