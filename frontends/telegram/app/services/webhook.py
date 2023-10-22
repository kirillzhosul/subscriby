from aiogram import Bot
from aiohttp.web import Request

from app.settings import TelegramSettings
from app.texts import T


async def webhook_handler(request: Request, bot: Bot):
    json = await request.json()
    event = json["event"]
    name = event["name"]
    payload = event["payload"]

    message = None
    match name:
        case "subscription.publish":
            p = payload["subscription"]
            message = T["subscription_created"].format(
                p["secret_key"], p["expires_date"], p["payload"]
            )
        case "subscription.revoke":
            p = payload["subscription"]
            message = T["subscription_revoked"].format(p["secret_key"], p["payload"])

    if not message:
        return
    for user_id in TelegramSettings().admin_ids:
        try:
            await bot.send_message(user_id, message)
        except Exception:
            continue
