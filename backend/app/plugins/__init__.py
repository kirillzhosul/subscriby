"""
    Custom plugins where you expected to write your own custom code
"""

from .bases import BaseAuthPlugin, BaseKPIPlugin, BasePayloadPlugin
from .custom_auth import CustomAuthPlugin
from .custom_kpi import CustomKPIPlugin
from .custom_payload import CustomPayloadPlugin

__all__ = [
    "CustomAuthPlugin",
    "CustomPayloadPlugin",
    "BasePayloadPlugin",
    "CustomKPIPlugin",
    "BaseKPIPlugin",
    "BaseAuthPlugin",
]
