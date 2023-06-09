from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from . import config
from .resources import lifespan
from .routers import hello

routers = [
    hello.router,
]

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    debug=config.DEBUG,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

for router in routers:
    app.include_router(router)
