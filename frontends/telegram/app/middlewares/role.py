from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.models.role import UserRole


class RoleMiddleware(BaseMiddleware):
    def __init__(self, admin_list: List[int]):
        self.admin_list = admin_list

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not getattr(event, "from_user", None):
            data["role"] = None
        elif event.from_user.id in self.admin_list:
            data["role"] = UserRole.ADMIN
        else:
            data["role"] = UserRole.USER

        result = await handler(event, data)

        del data["role"]
        return result
