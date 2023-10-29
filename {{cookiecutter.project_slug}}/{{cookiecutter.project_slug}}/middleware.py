from collections.abc import Callable
from secrets import token_urlsafe
from time import time

from fastapi import Request, Response
from fastapi.responses import PlainTextResponse
from hypercorn.logging import AccessLogAtoms
from loguru import logger

from . import config


async def log_request_middleware(request: Request, call_next: Callable) -> Response:
    """
    Uniquely identify each request and logs its processing time.
    """
    start_time = time()
    request_id: str = token_urlsafe(config.REQUEST_ID_LENGTH)
    exception = None

    # keep the same request_id in the context of all subsequent calls to logger
    with logger.contextualize(request_id=request_id):
        try:
            response = await call_next(request)
        except Exception as exc:
            exception = exc
            response = PlainTextResponse('Internal Server Error', status_code=500)
        final_time = time()
        elapsed = final_time - start_time
        response_dict = {
            'status': response.status_code,
            'headers': response.headers.raw,
        }
        atoms = AccessLogAtoms(request, response_dict, final_time)  # type: ignore
        try:
            response_length = int(atoms['B'])
        except ValueError:
            response_length = 0
        data = {
            'client': atoms['h'],
            'schema': atoms['S'],
            'protocol': atoms['H'],
            'method': atoms['m'],
            'path_with_query': atoms['Uq'],
            'status_code': response.status_code,
            'response_length': response_length,
            'elapsed': elapsed,
            'referer': atoms['f'],
            'user_agent': atoms['a'],
        }
        if not exception:
            logger.info('log request', **data)
        else:
            logger.opt(exception=exception).error('Unhandled exception', **data)
    response.headers['X-Request-ID'] = request_id
    response.headers['X-Processed-Time'] = str(elapsed)
    return response
