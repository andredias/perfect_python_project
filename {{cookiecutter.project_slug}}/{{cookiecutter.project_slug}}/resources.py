import logging
import sys
from string import ascii_uppercase

from loguru import logger

from . import config


async def startup() -> None:
    setup_logger()
    show_config()
    # connect to database
    logger.info('started...')


async def shutdown() -> None:
    # disconnect from database
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
