import json
from unittest.mock import patch

from fastapi import APIRouter, FastAPI
from httpx import AsyncClient
from pytest import CaptureFixture, fixture


@fixture
def app_with_logging_routes(app: FastAPI) -> FastAPI:
    """
    Modify the app to include some routes for testing logging.
    """
    router = APIRouter(prefix='/test_logging')

    @router.get('/info')
    async def info() -> dict[str, str]:
        return {'message': 'info'}

    @router.get('/divide')
    async def divide(a: int, b: int) -> float:
        return a / b

    app.include_router(router)
    return app


async def test_json_logging(
    app_with_logging_routes: FastAPI, client: AsyncClient, capsys: CaptureFixture
) -> None:
    """
    Test that the log is in JSON format.
    """
    with patch(
        '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
    ):  # prevents highlighting
        response = await client.get('/test_logging/info')
    assert response.status_code == 200
    assert response.json() == {'message': 'info'}

    log = json.loads(capsys.readouterr().err)
    assert {'time', 'level', 'message', 'source', 'request_id', 'elapsed'} <= set(log.keys())
    assert 'exception' not in log


async def test_logging_422_exception(
    app_with_logging_routes: FastAPI, client: AsyncClient, capsys: CaptureFixture
) -> None:
    """
    Test if the log contains the exception when the request is invalid.
    """
    with patch(
        '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
    ):  # prevents highlighting
        response = await client.get('/test_logging/divide', params={'a': 1.1, 'b': 0})
    assert response.status_code == 422
    detail = response.json()['detail']

    # there must be 2 log entries: 1 for the exception and 1 for the request
    text = capsys.readouterr().err
    position = text.index('\n}\n{\n')

    exception_log = json.loads(text[: position + 2])
    assert {'time', 'level', 'message', 'source', 'request_id', 'detail'} == set(
        exception_log.keys()
    )
    assert detail == exception_log['detail']

    request_log = json.loads(text[position + 3 :])
    assert {'time', 'level', 'message', 'source', 'request_id', 'elapsed'} <= set(
        request_log.keys()
    )
    assert 'exception' not in request_log


async def test_logging_500_exception(
    app_with_logging_routes: FastAPI, client: AsyncClient, capsys: CaptureFixture
) -> None:
    """
    Test if the log contains the exception when the request is invalid.
    """
    with patch(
        '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
    ):  # prevents highlighting
        response = await client.get('/test_logging/divide', params={'a': 1, 'b': 0})
    assert response.status_code == 500
    assert response.json()['detail'] == 'Internal Server Error'

    # there must be 2 log entries: 1 for the exception and 1 for the request
    text = capsys.readouterr().err
    position = text.index('\n}\n{\n')

    exception_log = json.loads(text[: position + 2])
    assert {'time', 'level', 'message', 'source', 'request_id', 'exception'} == set(
        exception_log.keys()
    )

    request_log = json.loads(text[position + 3 :])
    assert {'time', 'level', 'message', 'source', 'request_id', 'elapsed'} <= set(
        request_log.keys()
    )
    assert 'exception' not in request_log
