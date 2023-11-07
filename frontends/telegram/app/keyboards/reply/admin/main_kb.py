"""
    Keyboards for Telegram.
"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.texts import T

# Button names.
BUTTON_CREATE_NEW = T["btn_create"]
BUTTON_REVOKE_OLD = T["btn_revoke"]
BUTTON_KPI_ANALYTICS = T["btn_kpi"]
BUTTON_RENEW_OLD = T["btn_renew"]
BUTTON_KEY_INFO = T["btn_info"]


def get():
    """
    Keyboard for the main menu.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_KEY_INFO)],
            [KeyboardButton(text=BUTTON_CREATE_NEW)],
            [KeyboardButton(text=BUTTON_REVOKE_OLD)],
            [KeyboardButton(text=BUTTON_RENEW_OLD)],
            [KeyboardButton(text=BUTTON_KPI_ANALYTICS)],
        ],
        resize_keyboard=True,
    )
