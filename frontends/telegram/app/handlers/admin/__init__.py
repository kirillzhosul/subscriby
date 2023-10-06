from aiogram import Router

from . import start
from . import subscriptions

router = Router(name=__name__)

router.include_routers(
    start.router,
    subscriptions.router
)
