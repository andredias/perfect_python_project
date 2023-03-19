import os
from pathlib import Path
from subprocess import check_call
from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture
from sqlalchemy.engine.url import make_url

os.environ['ENV'] = 'testing'

from {{cookiecutter.project_slug }} import config  # noqa: E402
from {{cookiecutter.project_slug}}.main import app as _app  # noqa: E402
from {{cookiecutter.project_slug}}.models.user import get_all, insert  # noqa: E402
from {{cookiecutter.project_slug}}.resources import connect_database, db  # noqa: E402
from {{cookiecutter.project_slug}}.schemas.user import UserInfo, UserInsert  # noqa: E402


@fixture(scope='session')
async def init_test_db() -> None:
    """
    Initialize the database.
    """
    url = make_url(config.DATABASE_URL).set(database='postgres')
    db = Database(str(url))
    await connect_database(db)

    try:
        stmt = f"select 1 from pg_database where datname='{config.DB_NAME}'"
        db_exists = await db.execute(stmt)
        if db_exists and os.getenv('RECREATE_DB'):
            stmt = f'drop database {config.DB_NAME}'
            await db.execute(stmt)
            db_exists = False
        if not db_exists:
            stmt = f'create database {config.DB_NAME}'
            await db.execute(stmt)
    finally:
        await db.disconnect()
    check_call('alembic upgrade head'.split(), cwd=Path(__file__).parent.parent)
    return


@fixture(scope='session')
async def session_app(init_test_db: None) -> AsyncIterable[FastAPI]:
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
