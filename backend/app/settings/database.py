"""
    Database settings of the application
"""


from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Environment databases settings
    """

    class Config:
        env_prefix = "DATABASE_"

    # Core database (only postgresql)
    # example: 'postgres://user:pass@localhost:5432/foobar'
    postgres_dsn: PostgresDsn
