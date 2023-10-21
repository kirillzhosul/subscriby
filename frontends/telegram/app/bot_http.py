from functools import partial

from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from .bot import main_init
from .settings import Settings
from .texts import T

TELEGRAM_WEBHOOK_PATH = "/webhook"
SUBSCRIBY_WEBHOOK_PATH = "/hook-subscriby"

_bot: Bot


async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook()
    await bot.set_webhook(
        f"{Settings().subscriby_telegram_web_host}{TELEGRAM_WEBHOOK_PATH}",
    )


async def subscriby_webhook_handler(request: web.Request):
    json = await request.json()
    event_name = json["event_name"]

    if event_name == "subscription.publish":
        subscription = json["event_payload"]["subscription"]

        for user_id in Settings().subscriby_telegram_admin_ids:
            await _bot.send_message(
                user_id,
                T["subscription_created"].format(
                    subscription["secret_key"],
                    subscription["expires_date"],
                    subscription["payload"],
                ),
            )
    elif event_name == "subscription.revoke":
        subscription = json["event_payload"]["subscription"]
        for user_id in Settings().subscriby_telegram_admin_ids:
            await _bot.send_message(
                user_id,
                T["subscription_revoked"].format(
                    subscription["secret_key"],
                    subscription["payload"],
                ),
            )


def main() -> None:
    global _bot
    _bot, dp = main_init()
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=_bot,
    )
    webhook_requests_handler.register(app, path=TELEGRAM_WEBHOOK_PATH)
    app.router.add_post(SUBSCRIBY_WEBHOOK_PATH, subscriby_webhook_handler)
    setup_application(app, dp, bot=_bot)
    web.run_app(app, host="0.0.0.0", port=3000)
