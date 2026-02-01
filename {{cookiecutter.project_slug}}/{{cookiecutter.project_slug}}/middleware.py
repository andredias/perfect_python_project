from secrets import token_urlsafe
from time import time
from typing import Any, Final

from fastapi import Request, status
from fastapi.responses import PlainTextResponse
from loguru import logger
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from . import config
from . import resources as res
from .resources import connection_ctx


class LogRequestMiddleware:
    """
    Uniquely identify each request and logs its processing time.
    """

    def __init__(self, app: ASGIApp, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive, send)
        start_time = time()
        request_id: str = token_urlsafe(config.REQUEST_ID_LENGTH)
        response_status = None
        response_length = 0
        exception = None
        elapsed = 0.0

        async def send_wrapper(message: Message) -> None:
            nonlocal elapsed, response_status, response_length

            if message['type'] == 'http.response.start':
                response_status = message['status']
                headers = message.get('headers', [])
                elapsed = time() - start_time
                # Add our custom headers to the response
                headers.append((b'X-Request-ID', request_id.encode()))
                headers.append((b'X-Processed-Time', str(elapsed).encode()))
                message['headers'] = headers
            elif message['type'] == 'http.response.body':
                response_length += len(message.get('body', b''))
            await send(message)

        # keep the same request_id in the context of all subsequent calls to logger
        with logger.contextualize(request_id=request_id):
            try:
                await self.app(scope, receive, send_wrapper)
            except Exception as exc:
                exception = exc
                # Send error response
                error_response = PlainTextResponse('Internal Server Error', status_code=500)
                await error_response(scope, receive, send)

            # Log the request after processing
            query_string = request['query_string'].decode()
            path_with_qs = f'{request["path"]}?{query_string}' if query_string else request['path']
            data = {
                'remote_ip': request.headers.get('x-forwarded-for') or request['client'],
                'schema': request.headers.get('x-forwarded-proto') or request['scheme'],
                'protocol': request.get('http_version', 'ws'),
                'method': request.get('method', 'GET'),
                'path_with_query': path_with_qs,
                'status_code': response_status or 500,
                'response_length': response_length,
                'elapsed': elapsed,
                'referer': request.headers.get('referer', ''),
                'user_agent': request.headers.get('user-agent', ''),
            }
            if not exception:
                logger.info('log request', **data)
            else:
                logger.opt(exception=exception).error('Unhandled exception', **data)


COMMIT: Final[int] = 0
ROLLBACK: Final[int] = 1


class DatabaseConnectionMiddleware:
    """
    Ensures that the database connection is closed after the request is processed.
    """
    def __init__(self, app: ASGIApp, *args: Any, **kwargs: Any) -> None:  # noqa: ARG002
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope['type'] != 'http'
            or res.connection_ctx.get()  # the database connection will be managed in tests
        ):
            await self.app(scope, receive, send)
            return

        db_action: int = ROLLBACK

        async def send_wrapper(message: Message) -> None:
            nonlocal db_action, send

            if message['type'] == 'http.response.start':
                status_code = message['status']
                if status_code < status.HTTP_400_BAD_REQUEST:
                    db_action = COMMIT
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            if connection := res.connection_ctx.get():
                if db_action == COMMIT:
                    await connection.commit()
                else:
                    await connection.rollback()
                await connection.close()
                connection_ctx.set(None)
