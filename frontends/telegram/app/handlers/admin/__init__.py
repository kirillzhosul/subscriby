from aiogram import Router

from . import analytics, start, subscriptions

router = Router(name=__name__)

router.include_routers(start.router, subscriptions.router, analytics.router)
