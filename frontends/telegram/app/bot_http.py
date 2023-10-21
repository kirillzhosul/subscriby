from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from .bot import main_init
from .settings import Settings

TELEGRAM_WEBHOOK_PATH = "/webhook"
SUBSCRIBY_WEBHOOK_PATH = "/hook-subscriby"


async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook()
    await bot.set_webhook(
        f"{Settings().subscriby_telegram_web_host}{TELEGRAM_WEBHOOK_PATH}",
    )


async def subscriby_webhook_handler(request: web.Request):
    print("Webhook!", await request.json())


def main() -> None:
    bot, dp = main_init()
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=TELEGRAM_WEBHOOK_PATH)
    app.router.add_post(SUBSCRIBY_WEBHOOK_PATH, subscriby_webhook_handler)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=3000)
