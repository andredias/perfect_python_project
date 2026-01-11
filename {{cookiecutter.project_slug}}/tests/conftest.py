import os
from pathlib import Path
from subprocess import check_call
from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncConnection

os.environ['ENV'] = 'testing'

from {{cookiecutter.project_slug }} import config  # noqa: E402
from {{cookiecutter.project_slug }} import resources  # noqa: E402
from {{cookiecutter.project_slug}}.main import app as _app  # noqa: E402
from {{cookiecutter.project_slug}}.models.user import UserInfo, UserInsert, get_all, insert  # noqa: E402
from {{cookiecutter.project_slug}}.resources import get_db  # noqa: E402


@fixture(scope='session')
async def init_test_db() -> None:
    """
    Initialize the database.
    """
    assert '/test_' in config.DATABASE_URL
    # alembic/env.py creates the database if it doesn't exist
    check_call('alembic upgrade head'.split(), cwd=Path(__file__).parent.parent)


@fixture(scope='session')
async def app(init_test_db: None) -> AsyncIterable[FastAPI]:
    async with LifespanManager(_app):
        yield _app


@fixture
async def db_connection(app: FastAPI) -> AsyncIterable[AsyncConnection]:
    """
    Create a database connection for the test.
    """
    connection = await get_db()
    try:
        yield connection
    finally:
        await connection.rollback()
        await connection.close()
        resources.connection_ctx.set(None)


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://testserver') as client:
        yield client


@fixture
async def users(db_connection: AsyncConnection) -> list[UserInfo]:
    """
    Populate the database with users.
    """

    users = await get_all()
    if users:
        return users

    users_ = [
        UserInsert(
            name='Fulano de Tal',
            email='fulano@email.com',
            password='Paulo Paulada Power',
        ),
        UserInsert(
            name='Beltrano de Tal',
            email='beltrano@email.com',
            password='abcdefgh1234567890',
        ),
    ]

    for user in users_:
        await insert(user)
    await db_connection.commit()
    return await get_all()
