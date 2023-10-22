from aiogram import Router
from aiogram.types import Message

from app.texts import T

router = Router(name=__name__)


# Apply RoleFilter to only this handler
@router.message()
async def start_command(message: Message) -> None:
    await message.answer(T["not_admin"])
