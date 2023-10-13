
from fastapi import Request
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    This is a wrapper to the default RequestValidationException handler of FastAPI
    that logs the exception for easier debugging.
    """
    logger.info('request validation exception', detail=exc.errors())
    return await _request_validation_exception_handler(request, exc)
