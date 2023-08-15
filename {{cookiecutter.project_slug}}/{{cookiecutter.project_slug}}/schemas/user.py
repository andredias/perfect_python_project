import json
from typing_extensions import Annotated

from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator

from ..config import PASSWORD_MIN_LENGTH, PASSWORD_MIN_VARIETY


def check_password(password: str) -> str:
    errors = []
    if len(password) < PASSWORD_MIN_LENGTH:
        errors.append(f'Password length < {PASSWORD_MIN_LENGTH} chars')
    if len(set(password)) < PASSWORD_MIN_VARIETY:
        errors.append(f'Variety < {PASSWORD_MIN_VARIETY} chars')
    if errors:
        raise ValueError(json.dumps(errors))
    return password


Password = Annotated[str, AfterValidator(check_password)]


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserInsert(BaseModel):
    name: str
    email: EmailStr
    password: Password


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: Password | None = None
