import json

from pydantic import BaseModel, EmailStr, validator

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


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserInsert(BaseModel):
    name: str
    email: EmailStr
    password: str

    _password = validator('password', allow_reuse=True)(check_password)


class UserPatch(BaseModel):
    name: str | None
    email: EmailStr | None
    password: str | None

    _password = validator('password', allow_reuse=True)(check_password)
