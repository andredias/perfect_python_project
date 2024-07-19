import os
from pathlib import Path
from subprocess import check_call
from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

os.environ['ENV'] = 'testing'

from {{cookiecutter.project_slug }} import config  # noqa: E402
from {{cookiecutter.project_slug}}.main import app as _app  # noqa: E402
from {{cookiecutter.project_slug}}.models.user import UserInfo, UserInsert, get_all, insert  # noqa: E402
from {{cookiecutter.project_slug}}.resources import db  # noqa: E402


@fixture(scope='session', autouse=True)
def anyio_backend() -> str:
    return 'asyncio'


@fixture(scope='session')
async def init_test_db() -> None:
    """
    Initialize the database.
    """
    assert '/test_' in config.DATABASE_URL
    # alembic/env.py creates the database if it doesn't exist
    check_call('alembic upgrade head'.split(), cwd=Path(__file__).parent.parent)


@fixture(scope='session')
async def session_app(init_test_db: None) -> AsyncIterable[FastAPI]:
    async with LifespanManager(_app):
        yield _app


@fixture
async def app(session_app: FastAPI) -> AsyncIterable[FastAPI]:
    with db.force_rollback():
        yield session_app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


@fixture(scope='session')
async def users(session_app: FastAPI) -> list[UserInfo]:
    """
    Populate the database with users.
    """

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

    return await get_all()
