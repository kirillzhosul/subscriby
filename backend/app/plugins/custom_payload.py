"""
Custom plugin for payload validation / parsing
"""

from pydantic import BaseModel, ValidationError

from .bases import BaseModelPayload, BasePayloadPlugin


class CustomPayloadModel(BaseModelPayload):
    """
    Model that represents custom payload filter
    """


class CustomPayloadPlugin(BasePayloadPlugin):
    """
    Custom plugin for payload validation / parsing
    """

    T: type[BaseModel] = CustomPayloadModel

    def __call__(self, payload: str) -> str:
        try:
            p = self.T.model_validate_json(json_data=payload)
        except ValidationError:
            p = self.T()

        return p.model_dump_json(
            exclude_none=False,
            exclude_unset=False,
            exclude_defaults=False,
        )
