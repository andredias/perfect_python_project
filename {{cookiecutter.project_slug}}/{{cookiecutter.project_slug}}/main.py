from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from . import config  # noqa: F401
from .exception_handlers import request_validation_exception_handler
from .resources import lifespan
from .routers import hello, user
from .middleware import (
    DatabaseConnectionMiddleware,
    LogRequestMiddleware,
)

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    lifespan=lifespan,
)

routers = (
    hello.router,
    user.router,
)

for router in routers:
    app.include_router(router)

app.add_middleware(DatabaseConnectionMiddleware)
app.add_middleware(LogRequestMiddleware)
# type annotation problem. See: https://github.com/encode/starlette/pull/2403
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)  # type: ignore
