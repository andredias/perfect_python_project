import os
from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pytest import fixture

os.environ['ENV'] = 'testing'

from {{cookiecutter.project_slug}}.main import app as _app  # noqa: E402


@fixture
async def app() -> AsyncIterable[FastAPI]:
    """
    Create a FastAPI instance.
    """
    async with LifespanManager(_app):
        yield _app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://testserver') as client:
        yield client
