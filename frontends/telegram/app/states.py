"""
    States for the Telegram.
"""
from aiogram.fsm.state import State, StatesGroup


class PublishSubscription(StatesGroup):
    days = State()
    payload = State()
