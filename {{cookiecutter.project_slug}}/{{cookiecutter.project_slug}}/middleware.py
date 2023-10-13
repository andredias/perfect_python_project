import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from hypercorn.logging import AccessLogAtoms
from loguru import logger


async def log_request_middleware(request: Request, call_next: Callable) -> Response:
    """
    This middleware will log all requests and their processing time.
    """
    # Create a request ID
    request_id = str(uuid.uuid4())

    # Add context to all loggers in all views
    start_time = time.time()
    with logger.contextualize(request_id=request_id):
        response = await call_next(request)
        final_time = time.time()
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
