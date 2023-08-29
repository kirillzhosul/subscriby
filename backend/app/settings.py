"""
    Environment settings for `Subscriby`
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Environment settings for `Subscriby`
    """

    postgres_name: str = "subscriby"
    postgres_user: str = "subscriby"
    postgres_password: str = "subscriby"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    subscriby_auth_method: str = "none"
    subscriby_auth_secret: str | None = None  # For `secret` auth method.
    subscriby_expires_date_format: str = "%Y.%m.%d"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self._database_connection_string()}"

    @property
    def database_async_url(self) -> str:
        return f"postgresql+asyncpg://{self._database_connection_string()}"

    def _database_connection_string(self) -> str:
        return f"{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_name}"
