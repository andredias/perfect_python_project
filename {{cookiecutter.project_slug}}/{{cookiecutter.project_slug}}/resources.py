from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any

from fastapi import FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine
from tenacity import RetryError, retry, stop_after_delay, wait_exponential

from . import config
from .logging import init_loguru


engine: AsyncEngine = None  # type: ignore[assignment]
connection_ctx: ContextVar[AsyncConnection | None] = ContextVar('connection_ctx', default=None)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:  # noqa: ARG001
    await startup()
    try:
        yield
    finally:
        await shutdown()


async def startup() -> None:
    init_loguru()
    show_config()

    init_database()
    await test_database_connection()
    logger.info('started...')


async def shutdown() -> None:
    await engine.dispose()
    logger.info('...shutdown')


def show_config() -> None:
    config_vars = {key: getattr(config, key) for key in sorted(dir(config)) if key.isupper()}
    logger.debug('config vars', **config_vars)


def init_database() -> None:
    '''
    Initialize the database connection engine.
    '''
    # see: https://hevalhazalkurt.com/blog/connection-pooling-deep-dive-with-sqlalchemy/
    global engine  # noqa: PLW0603
    engine = create_async_engine(config.DATABASE_URL, echo=config.DEBUG)


async def test_database_connection() -> None:

    @retry(stop=stop_after_delay(3), wait=wait_exponential(multiplier=0.2))
    async def _connect_to_db() -> None:
        logger.info('Connecting to the database...')
        async with engine.connect():
            pass

    try:
        await _connect_to_db()
    except RetryError:
        logger.error('Could not connect to the database.')
        raise


async def get_db() -> AsyncConnection:
    '''
    Get a database connection. Reuses the same connection within the same request.
    '''
    connection = connection_ctx.get()
    # check if the connection is closed
    if connection is None:
        connection = await engine.connect()
        connection_ctx.set(connection)
    return connection


async def db_execute(query: Any) -> Any:
    '''
    Execute a database query using the current request's connection.
    '''
    connection = await get_db()
    return await connection.execute(query)
