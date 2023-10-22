"""
    Entry point of the Telegram bot
"""

from logging import INFO, basicConfig
from sys import stdout

from app.bot import start_http

if __name__ == "__main__":
    basicConfig(level=INFO, stream=stdout)
    start_http()
