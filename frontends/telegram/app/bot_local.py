from .bot import main_init


async def main() -> None:
    """
    Entry point of the bot, should be ran with Docker
    """
    bot, dp = main_init()
    await dp.start_polling(bot)
