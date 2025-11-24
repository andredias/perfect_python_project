from collections.abc import Callable
from secrets import token_urlsafe
from time import time

from fastapi import Request, Response
from fastapi.responses import PlainTextResponse
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
        response_length = request.headers.get('content-length', 0)
        query_string = request['query_string'].decode()
        path_with_qs = request['path'] + ('?' + query_string if query_string else '')
        data = {
            'remote_ip': request.headers.get('x-forwarded-for') or request['client'],
            'schema': request.headers.get('x-forwarded-proto') or request['scheme'],
            'protocol': request.get('http_version', 'ws'),
            'method': request.get('method', 'GET'),
            'path_with_query': path_with_qs,
            'status_code': response.status_code,
            'response_length': response_length,
            'elapsed': elapsed,
            'referer': request.headers.get('referer', ''),
            'user_agent': request.headers.get('user-agent', ''),
        }
        if not exception:
            logger.info('log request', **data)
        else:
            logger.opt(exception=exception).error('Unhandled exception', **data)
    response.headers['X-Request-ID'] = request_id
    response.headers['X-Processed-Time'] = str(elapsed)
    return response
