from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.reply.admin import main_kb
from app.roles import RoleFilter, UserRole
from app.texts import T

router = Router(name=__name__)


# Apply RoleFilter to only this handler
@router.message(CommandStart(), RoleFilter(UserRole.ADMIN))
async def start_command(message: Message) -> None:
    """
    Handler for `/start` command.
    """
    await message.answer(
        T["welcome"].format(message.from_user.full_name), reply_markup=main_kb.get()
    )
