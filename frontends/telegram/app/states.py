"""
    States for the Telegram.
"""
from aiogram.dispatcher.filters.state import StatesGroup, State


class PublishSubscription(StatesGroup):
    days = State()
    payload = State()
