from collections.abc import Callable
from secrets import token_urlsafe
from time import time

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from hypercorn.logging import AccessLogAtoms
from loguru import logger

from . import config


async def log_request_middleware(request: Request, call_next: Callable) -> Response:
    """
    Uniquely identify each request and logs its processing time.
    """
    start_time = time()
    request_id: str = token_urlsafe(config.REQUEST_ID_LENGTH)

    # keep the same request_id in the context of all subsequent calls to logger
    with logger.contextualize(request_id=request_id):
        response = await call_next(request)
        final_time = time()
        elapsed = final_time - start_time
        response_dict = {
            'status': response.status_code,
            'headers': response.headers.raw,
        }
        atoms = AccessLogAtoms(request, response_dict, final_time)  # type: ignore
        logger.info(
            'log request',
            client=atoms['h'],
            schema=atoms['S'],
            protocol=atoms['H'],
            method=atoms['m'],
            path_with_query=atoms['Uq'],
            status_code=response.status_code,
            response_length=atoms['b'],
            elapsed=elapsed,
            referer=atoms['f'],
            user_agent=atoms['a'],
        )
    return response


async def generic_exception_handler(request: Request, call_next: Callable) -> JSONResponse:
    """
    Ideally, it should be an exception handler for all uncaught exceptions.
    However, it does not work as reported in this issue:
    https://github.com/tiangolo/fastapi/discussions/8647#discussioncomment-5153245
    """
    try:
        return await call_next(request)
    except Exception:
        logger.exception('uncaught exception')
        return JSONResponse(content={'detail': 'Internal Server Error'}, status_code=500)