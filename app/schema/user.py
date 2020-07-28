from pydantic import validator, EmailStr, Field
import re

from app.setting import settings
from .mixin import AppSchemaBase


def validate_password(
        password: str,
        minLength: int = settings.PASSWORD_MIN_LENGTH
        ) -> bool:

    if (len(password) < minLength):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[_@$]", password):
        return False
    elif re.search("\s", password): # noqa
        return False

    return True


class RegisterLocal(AppSchemaBase):
    email: EmailStr = Field(..., alias='username')
    password: str

    @validator('password')
    def check_password(cls, v):
        if v is not None and not validate_password(v):
            raise ValueError(
                'Your password does not satisfy the current policy requirements.'
            )
        return v


class RegisterProvider(AppSchemaBase):
    email: EmailStr
    sub: str
    provider: str


class CreateUser(AppSchemaBase):
    email: str
    password_hash: str = None
    sub: str = None
    provider: str = None


class UpdateUser(CreateUser):
    email: EmailStr = None
