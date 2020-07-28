from .mixin import AppSchemaBase


class Token(AppSchemaBase):
    access_token: str
    token_type: str
