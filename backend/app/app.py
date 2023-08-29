"""
    FastAPI application.
"""
from fastapi import FastAPI

from .routers.subscription import router
from .database.core import create_all


def create_application() -> FastAPI:
    """
    Returns prepared and ready to run application.
    """
    app = FastAPI()
    app.include_router(router)
    app.add_event_handler("startup", create_all)
    return app
