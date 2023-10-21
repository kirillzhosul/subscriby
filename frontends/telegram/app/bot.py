"""
    Main Telegram bot for Subscriby.
"""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .handlers import admin, user
from .middlewares.role import RoleMiddleware
from .settings import Settings


def main_init() -> tuple[Bot, Dispatcher]:
    token = Settings().subscriby_telegram_token
    bot = Bot(token=token, parse_mode="html")
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.outer_middleware(
        RoleMiddleware(admin_list=Settings().subscriby_telegram_admin_ids)
    )
    dp.callback_query.outer_middleware(
        RoleMiddleware(admin_list=Settings().subscriby_telegram_admin_ids)
    )

    dp.include_routers(
        admin.router,
        user.router,
    )

    return bot, dp
