"""
    Keyboards for Telegram.
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Button names.
BUTTON_CREATE_NEW = "🛒 Create new"
BUTTON_REVOKE_OLD = "🔸 Revoke old"


def get():
    """
    Keyboard for the main menu.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_CREATE_NEW)],
            [KeyboardButton(text=BUTTON_REVOKE_OLD)]
        ],
        resize_keyboard=True
    )
    return keyboard
