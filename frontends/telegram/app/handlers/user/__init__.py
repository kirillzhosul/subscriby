from aiogram import Router

from . import start

router = Router(name=__name__)

router.include_routers(
    start.router,
)
