"""
    Routers for FastAPI
"""

from fastapi import APIRouter, FastAPI

from . import analytics, subscription

root_router = APIRouter()
root_router.include_router(analytics.router)
root_router.include_router(subscription.router)


def include_routers(app: FastAPI) -> None:
    """
    Includes all routers to the application
    """
    app.include_router(root_router)


__all__: list[str] = ["root_router", "include_routers"]
