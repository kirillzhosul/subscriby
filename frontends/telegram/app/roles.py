"""
    Role system of the bot
"""
from enum import Enum
from typing import Any, Awaitable, Callable, Collection, Dict, List, Union

from aiogram import BaseMiddleware
from aiogram.filters import Filter
from aiogram.types import TelegramObject, User


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class RoleFilter(Filter):
    def __init__(self, role: Union[UserRole, Collection[UserRole]]) -> None:
        self.roles = {role} if isinstance(role, UserRole) else set(role)

    async def __call__(
        self,
        *args,
        event_from_user: User,
        role: Union[None, UserRole, Collection[UserRole]] = None,
        **kwargs
    ) -> bool:
        return role in self.roles


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
