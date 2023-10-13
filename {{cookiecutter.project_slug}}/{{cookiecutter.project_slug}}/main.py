from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from . import config
from .exception_handlers import request_validation_exception_handler
from .resources import lifespan
from .routers import hello
from .middleware import log_request_middleware

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    debug=config.DEBUG,
    lifespan=lifespan,
)

routers = (
    hello.router,
)

for router in routers:
    app.include_router(router)

app.middleware('http')(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
