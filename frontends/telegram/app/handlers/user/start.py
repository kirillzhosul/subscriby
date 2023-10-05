from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name=__name__)


# Apply RoleFilter to only this handler
@router.message(CommandStart())
async def start_command(message: Message) -> None:
    """
    Handler for `/start` command.
    """
    await message.answer("<b>Sorry, you are not an admin!</b>")
