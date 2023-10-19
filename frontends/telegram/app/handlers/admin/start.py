from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.telegram.app.filters.role import RoleFilter
from app.telegram.app.keyboards.reply.admin import main_kb
from app.telegram.app.models.role import UserRole

router = Router(name=__name__)


# Apply RoleFilter to only this handler
@router.message(CommandStart(), RoleFilter(UserRole.ADMIN))
async def start_command(message: Message) -> None:
    """
    Handler for `/start` command.
    """
    await message.answer(
        f"Welcome to <b>Subscriby</b>, <i>{message.from_user.full_name}</i>!",
        reply_markup=main_kb.get(),
    )
