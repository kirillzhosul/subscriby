"""
    Keyboards for Telegram.
"""
from aiogram.types import ReplyKeyboardMarkup

# Button names.
BUTTON_CREATE_NEW = "🛒 Create new"
BUTTON_REVOKE_OLD = "🔸 Revoke old"


def main_menu():
    """
    Keyboard for the main menu.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(BUTTON_CREATE_NEW)
    keyboard.row(BUTTON_REVOKE_OLD)
    return keyboard
