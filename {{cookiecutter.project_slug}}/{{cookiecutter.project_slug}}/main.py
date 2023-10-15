from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from . import config  # noqa: F401
from .exception_handlers import request_validation_exception_handler
from .resources import lifespan
from .routers import hello
from .middleware import generic_exception_handler, log_request_middleware

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    lifespan=lifespan,
)

routers = (
    hello.router,
)

for router in routers:
    app.include_router(router)

app.middleware('http')(generic_exception_handler)
app.middleware('http')(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
