"""
    Handlers for the FastAPI
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request

from .database.core import create_all
from .services import WebhookEventType, broadcast_webhook_event


async def exception_handler(request: Request, exception: Exception) -> None:
    """
    Exception handler for whole system (hook info)
    """
    await broadcast_webhook_event(
        WebhookEventType.server_error, {"exception": repr(exception)}
    )
    return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)


async def startup_handler() -> None:
    """
    Exception handler for whole system (hook info)
    """

    create_all()
    await broadcast_webhook_event(WebhookEventType.server_startup, {})


def add_handlers(app: FastAPI) -> None:
    """
    Adds handlers to the application
    """
    app.add_exception_handler(Exception, exception_handler)
    app.add_event_handler("startup", startup_handler)
