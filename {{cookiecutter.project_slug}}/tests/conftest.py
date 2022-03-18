from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from {{cookiecutter.project_slug}}.main import app as _app


@fixture
async def app() -> AsyncIterable[FastAPI]:
    """
    Create a FastAPI instance.
    """
    async with LifespanManager(_app):
        yield _app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(
        app=app,
        base_url='http://testserver',
        headers={'Content-Type': 'application/json'},
    ) as client:
        yield client
