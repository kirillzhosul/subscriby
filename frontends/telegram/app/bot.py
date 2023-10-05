"""
    Main Telegram bot for Subscriby.
"""
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot

from .settings import Settings
from .middlewares.role import RoleMiddleware
from .handlers import admin, user


async def main() -> None:
    """
    Entry point of the bot, should be ran with Docker
    """
    token = Settings().subscriby_telegram_token
    bot = Bot(token=token, parse_mode="html")
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.outer_middleware(RoleMiddleware(admin_list=Settings().subscriby_telegram_admin_ids))
    dp.callback_query.outer_middleware(RoleMiddleware(admin_list=Settings().subscriby_telegram_admin_ids))

    dp.include_routers(
        admin.router,
        user.router,
    )

    await dp.start_polling(bot)
