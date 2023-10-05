from typing import Union, Collection

from aiogram.filters import Filter
from aiogram.types import User

from frontends.telegram.app.models.role import UserRole


class RoleFilter(Filter):
    def __init__(self, role: Union[UserRole, Collection[UserRole]]) -> None:
        if isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def __call__(
            self,
            *args,
            event_from_user: User,
            role: Union[None, UserRole, Collection[UserRole]] = None,
            **kwargs
    ) -> bool:
        return role in self.roles
