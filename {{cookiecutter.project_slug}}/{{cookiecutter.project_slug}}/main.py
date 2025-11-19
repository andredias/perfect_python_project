from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from . import config  # noqa: F401
from .exception_handlers import request_validation_exception_handler
from .middleware import log_request_middleware
from .resources import lifespan
from .routers import hello, root

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    lifespan=lifespan,
    default_response_class=HTMLResponse,
)

app.mount('/static', StaticFiles(directory=config.STATIC_DIR), name='static')

routers = (
    root.router,
    hello.router,
)

for router in routers:
    app.include_router(router)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_request_middleware)
# type annotation problem. See: https://github.com/encode/starlette/pull/2403
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore
