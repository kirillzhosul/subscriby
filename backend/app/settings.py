"""
    Environment settings for `Subscriby`
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Environment settings for `Subscriby`
    """

    class Config:
        env_prefix = "SUBSCRIBY_"

    auth_method: str = "none"
    auth_secret: str | None = None  # For `secret` auth method.
    date_format: str = "%Y.%m.%d"
    webhook_targets: list[str] = []


class DatabaseSettings(BaseSettings):
    """
    Environment database settings for `Subscriby`
    """

    class Config:
        env_prefix = "DATABASE_"

    name: str
    user: str
    host: str
    port: int
    password: str

    @property
    def url(self) -> str:
        return f"postgresql://{self.raw_url}"

    @property
    def raw_url(self) -> str:
        return f"{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_name}"
