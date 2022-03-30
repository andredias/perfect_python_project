import logging
import sys
from string import ascii_uppercase

from databases import Database
from loguru import logger
from sqlalchemy import create_engine
from tenacity import RetryError, retry, stop_after_delay, wait_exponential

from . import config
from .models import metadata

db = Database(config.DATABASE_URL, force_rollback=config.TESTING)


async def startup() -> None:
    setup_logger()
    show_config()
    await start_database()
    logger.info('started...')


async def shutdown() -> None:
    await db.disconnect()
    logger.info('...shutdown')


def setup_logger() -> None:
    """
    Configure Loguru's logger
    """
    _intercept_standard_logging_messages()
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr,
        level=config.LOG_LEVEL,
        colorize=True,
        backtrace=config.DEBUG,
        enqueue=True,
    )  # reinsert it to make it run in a different thread


def _intercept_standard_logging_messages() -> None:
    """
    Intercept standard logging messages toward loguru's logger
    ref: https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
    """

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).no
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back  # type: ignore
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def show_config() -> None:
    config_vars = {
        key: getattr(config, key)
        for key in sorted(dir(config))
        if key[0] in ascii_uppercase
    }
    logger.debug(config_vars)
    return


async def connect_database(database: Database) -> None:
    @retry(stop=stop_after_delay(3), wait=wait_exponential(multiplier=0.2))
    async def _connect_to_db() -> None:
        logger.debug('Connecting to the database...')
        await database.connect()

    try:
        await _connect_to_db()
    except RetryError:
        logger.error('Could not connect to the database.')
        raise


def create_db() -> None:
    engine = create_engine(config.DATABASE_URL, echo=config.TESTING)
    metadata.create_all(engine, checkfirst=True)


async def start_database() -> None:
    await connect_database(db)
    create_db()
    # migrate_db()
