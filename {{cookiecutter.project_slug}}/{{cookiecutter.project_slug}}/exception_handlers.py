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
    method = request.get('method', 'GET')
    query_string = request['query_string'].decode()
    path_with_query = request['path'] + ('?' + query_string if query_string else '')
    logger.info('request validation exception', method=method, path_with_query=path_with_query, detail=exc.errors())
    return await _request_validation_exception_handler(request, exc)
