from typing import Collection, Union

from aiogram.filters import Filter
from aiogram.types import User

from app.telegram.app.models.role import UserRole


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
