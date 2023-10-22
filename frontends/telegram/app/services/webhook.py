from aiogram import Bot
from aiohttp.web import Request

from app.settings import TelegramSettings
from app.texts import T


async def webhook_handler(request: Request, bot: Bot):
    json = await request.json()
    event_name = json["event_name"]

    message = None
    match event_name:
        case "subscription.publish":
            subscription = json["event_payload"]["subscription"]
            message = T["subscription_created"].format(
                subscription["secret_key"],
                subscription["expires_date"],
                subscription["payload"],
            )
        case "subscription.revoke":
            subscription = json["event_payload"]["subscription"]
            message = T["subscription_revoked"].format(
                subscription["secret_key"],
                subscription["payload"],
            )
        case _:
            return

    for user_id in TelegramSettings().admin_ids:
        await bot.send_message(user_id, message)
