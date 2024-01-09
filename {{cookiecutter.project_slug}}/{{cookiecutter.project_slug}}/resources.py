from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from jinja2_fragments.fastapi import Jinja2Blocks as Jinja2Templates
from loguru import logger

from . import config
from .logging import init_loguru

templates = Jinja2Templates(
    directory=config.TEMPLATE_DIR, autoescape=True, trim_blocks=True, lstrip_blocks=True
)


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
    # insert here calls to connect to database and other services
    logger.info('started...')


async def shutdown() -> None:
    # insert here calls to disconnect from database and other services
    logger.info('...shutdown')


def show_config() -> None:
    config_vars = {key: getattr(config, key) for key in sorted(dir(config)) if key.isupper()}
    logger.debug('config vars', **config_vars)
