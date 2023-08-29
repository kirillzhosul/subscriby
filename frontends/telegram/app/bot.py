"""
    Main Telegram bot for Subscriby.
"""

from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot

from .settings import Settings
from .handlers import register_handlers

# Initializing bot with dispatcher.
token = Settings().subscriby_telegram_token
bot = Bot(token=token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
register_handlers(dp)


async def main() -> None:
    """
    Entry point of the bot, should be ran with Docker
    """
    await dp.start_polling(bot)
