"""
    States for the Telegram.
"""
from aiogram.fsm.state import StatesGroup, State


class PublishSubscription(StatesGroup):
    days = State()
    payload = State()
