"""
    States for the Telegram.
"""

from aiogram.fsm.state import State, StatesGroup


class PublishSubscription(StatesGroup):
    days = State()
    price = State()


class RevokeSubscription(StatesGroup):
    key = State()


class InfoSubscription(StatesGroup):
    key = State()


class RenewSubscription(StatesGroup):
    key = State()
    days = State()


class KPIAnalytics(StatesGroup):
    days = State()
