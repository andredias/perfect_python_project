from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from . import config
from .resources import lifespan
from .routers import hello, user

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    debug=config.DEBUG,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

routers = (
    hello.router,
    user.router,
)

for router in routers:
    app.include_router(router)
