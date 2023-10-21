from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.texts import T

router = Router(name=__name__)


# Apply RoleFilter to only this handler
@router.message(CommandStart())
async def start_command(message: Message) -> None:
    """
    Handler for `/start` command.
    """
    await message.answer(T["not_admin"])
