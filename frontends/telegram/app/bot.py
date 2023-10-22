"""
    Main Telegram bot for Subscriby.
"""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from .handlers import admin, user
from .roles import RoleMiddleware
from .services.webhook import webhook_handler
from .settings import SubscribySettings, TelegramSettings

_bot: Bot
_dp: Dispatcher


def create_bot():
    global _dp, _bot
    token = TelegramSettings().token
    _bot = Bot(token=token, parse_mode="html")
    _dp = Dispatcher(storage=MemoryStorage())

    admin_ids = TelegramSettings().admin_ids
    _dp.message.outer_middleware(RoleMiddleware(admin_list=admin_ids))
    _dp.callback_query.outer_middleware(RoleMiddleware(admin_list=admin_ids))

    _dp.include_routers(admin.router, user.router)


async def subscriby_webhook_handler(request: web.Request):
    await webhook_handler(request, _bot)


async def on_startup(*args, **kwargs) -> None:
    settings = TelegramSettings()
    print("hook set to", f"{settings.web_host}{settings.hook_path}")
    await _bot.set_webhook(f"{settings.web_host}{settings.hook_path}")


def start_http() -> None:
    create_bot()
    settings = TelegramSettings()
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=_dp, bot=_bot)
    webhook_requests_handler.register(app, path=settings.hook_path)
    app.router.add_post(SubscribySettings().hook_path, subscriby_webhook_handler)
    app.on_startup.append(on_startup)
    setup_application(app, _dp, bot=_bot)
    web.run_app(app, host=settings.http_internal_host, port=settings.http_internal_port)
