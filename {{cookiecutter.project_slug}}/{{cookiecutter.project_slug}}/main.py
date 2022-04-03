from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from . import config
from .resources import shutdown, startup
from .routers import hello, user

routers = [
    hello.router,
    user.router,
]

origins = [
    '*',
]

app = FastAPI(
    title='{{cookiecutter.project_name}}',
    debug=config.DEBUG,
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['x-csrf-token'],
)


for router in routers:
    app.include_router(router)


@app.on_event('startup')
async def startup_event() -> None:
    await startup()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await shutdown()
