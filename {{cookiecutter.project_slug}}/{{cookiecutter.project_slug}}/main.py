from fastapi import FastAPI

from . import config
from .resources import lifespan
from .routers import hello

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
