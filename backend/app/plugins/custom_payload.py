"""
Custom plugin for payload validation / parsing
"""

from pydantic import BaseModel, ValidationError

from .bases import BasePayloadPlugin


class CustomPayloadModel(BaseModel):
    """
    Model that represents custom payload filter
    """

    version: int = 1


class CustomPayloadPlugin(BasePayloadPlugin):
    """
    Custom plugin for payload validation / parsing
    """

    def __call__(self, payload: str) -> str:
        try:
            return CustomPayloadModel.model_validate_json(
                json_data=payload
            ).model_dump_json()
        except ValidationError:
            return CustomPayloadModel().model_dump_json()
