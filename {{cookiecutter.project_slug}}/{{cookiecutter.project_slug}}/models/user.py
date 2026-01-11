from typing import Annotated
from uuid import UUID

import orjson as json
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator
from sqlalchemy import Column, String, Table, Unicode
from sqlalchemy.dialects.postgresql import UUID as UUID_
from uuid_extensions import uuid7

from .. import config
from ..resources import db_execute
from . import metadata

crypt_ctx = CryptContext(schemes=['argon2'])


User = Table(
    'user',
    metadata,
    Column('id', UUID_, primary_key=True),
    Column('name', Unicode, nullable=False),
    Column('email', Unicode, nullable=False, unique=True),
    Column('password_hash', String, nullable=False),
)


def check_password(password: str | None) -> str | None:
    """
    Valida senha. Se a senha for None e passou pela validação do Pydantic,
    então deve ter sido usada no UserPatch e a senha não foi alterada.
    """
    if password is None:
        return None
    errors = []
    if len(password) < config.PASSWORD_MIN_LENGTH:
        errors.append(f'Password length < {config.PASSWORD_MIN_LENGTH} chars')
    if len(set(password)) < config.PASSWORD_MIN_VARIETY:
        errors.append(f'Variety < {config.PASSWORD_MIN_VARIETY} chars')
    if errors:
        raise ValueError(json.dumps(errors))
    return password


class UserInfo(BaseModel):
    id: UUID
    name: str
    email: EmailStr


class UserInsert(BaseModel):
    name: str
    email: EmailStr
    password: Annotated[str, AfterValidator(check_password)]


class UserPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: Annotated[str | None, AfterValidator(check_password)] = None


async def get_all(limit: int = config.QUERY_LIMIT, offset: int = 0) -> list[UserInfo]:
    query = User.select().limit(limit).offset(offset)
    result = await db_execute(query)
    return [UserInfo(**r._mapping) for r in result]


async def get_user_by_email(email: str) -> UserInfo | None:
    query = User.select().where(User.c.email == email)
    result = (await db_execute(query)).first()
    return UserInfo(**result._mapping) if result else None


async def get_user_by_login(email: str, password: str) -> UserInfo | None:
    query = User.select().where(User.c.email == email)
    result = (await db_execute(query)).first()
    if result and crypt_ctx.verify(password, result._mapping['password_hash']):
        return UserInfo(**result._mapping)
    return None


async def get_user(id: UUID) -> UserInfo | None:
    query = User.select().where(User.c.id == id)
    result = (await db_execute(query)).first()
    if result:
        return UserInfo(**result._mapping)
    return None


async def insert(user: UserInsert) -> UUID:
    fields = user.model_dump()
    password = fields.pop('password')
    if password:
        fields['password_hash'] = crypt_ctx.hash(password)
    fields['id'] = uuid7()
    stmt = User.insert().values(fields)
    await db_execute(stmt)
    return fields['id']


async def update(id: UUID, patch: UserPatch) -> None:
    fields = patch.model_dump(exclude_unset=True)
    if not fields:
        return
    if 'password' in fields:
        password = fields.pop('password')
        fields['password_hash'] = crypt_ctx.hash(password)
    stmt = User.update().where(User.c.id == id).values(**fields)
    await db_execute(stmt)


async def delete(id: UUID) -> None:
    stmt = User.delete().where(User.c.id == id)
    await db_execute(stmt)
