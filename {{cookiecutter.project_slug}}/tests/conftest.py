from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from {{cookiecutter.project_slug}}.main import app as _app
from {{cookiecutter.project_slug}}.models.user import get_all, insert
from {{cookiecutter.project_slug}}.resources import db
from {{cookiecutter.project_slug}}.schemas.user import UserInfo, UserInsert


@fixture(scope='session')
async def session_app() -> AsyncIterable[FastAPI]:
    """
    Create a FastAPI instance.
    """
    async with LifespanManager(_app):
        yield _app


@fixture
async def app(session_app: FastAPI) -> AsyncIterable[FastAPI]:
    async with db.transaction(force_rollback=True):
        yield session_app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(
        app=app,
        base_url='http://testserver',
        headers={'Content-Type': 'application/json'},
    ) as client:
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
