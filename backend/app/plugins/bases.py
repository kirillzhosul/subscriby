"""
    Base classes for plugins.
"""
from abc import abstractmethod, ABC

from fastapi import Request


class BaseAuthPlugin(ABC):
    """
    Base plugin for auth check
    """

    @abstractmethod
    def __call__(self, secret_key: str, request: Request) -> bool:
        ...


class BasePayloadPlugin(ABC):
    """
    Base plugin for payload validation / parsing
    """

    @abstractmethod
    def __call__(self, payload: str) -> str:
        ...
