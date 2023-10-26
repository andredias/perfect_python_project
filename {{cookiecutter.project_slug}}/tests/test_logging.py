import json
from typing import AsyncIterable
from unittest.mock import patch

from fastapi import APIRouter, FastAPI, HTTPException, status
from httpx import AsyncClient
from pytest import CaptureFixture, fixture

basic_log_fields = {
    'timestamp',
    'level',
    'message',
    'source',
    'request_id',
    'method',
    'path_with_query',
}
failed_validation_log_fields = basic_log_fields | {'detail'}
request_log_fields = basic_log_fields | {'protocol', 'schema', 'elapsed', 'status_code'}
exception_log_fields = request_log_fields | {'exception'}


@fixture(scope='module')
async def logging_client() -> AsyncIterable[AsyncClient]:
    """
    Modify the app to include some routes for testing logging.
    """
    from {{cookiecutter.project_slug}}.logging import init_loguru
    from {{cookiecutter.project_slug}}.main import (
        BaseHTTPMiddleware,
        RequestValidationError,
        log_request_middleware,
        request_validation_exception_handler,
    )

    router = APIRouter()

    @router.get('/info')
    async def info() -> dict[str, int]:
        return {'data': 1234}

    @router.get('/divide')
    async def divide(a: int, b: int) -> float:
        return a / b

    @router.get('/http_exception')
    async def raise_http_exception(code: int) -> None:
        raise HTTPException(status_code=code)

    app = FastAPI()
    app.include_router(router)
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_request_middleware)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)

    init_loguru()

    async with AsyncClient(app=app, base_url='http://test_logging') as client:
        yield client

    return


async def test_json_logging(
    logging_client: AsyncClient, capsys: CaptureFixture
) -> None:
    """
    Test that the log is in JSON format.
    """
    with patch(
        '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
    ):  # prevents highlighting
        response = await logging_client.get('/info')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'data': 1234}

    log = json.loads(capsys.readouterr().err)
    assert request_log_fields <= set(log.keys())
    assert log['level'] == 'INFO'
    assert 'exception' not in log


async def test_logging_422_exception(
    logging_client: AsyncClient, capsys: CaptureFixture
) -> None:
    """
    Test if the log contains the exception when the request is invalid.
    """
    with patch(
        '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
    ):  # prevents highlighting
        response = await logging_client.get('/divide', params={'a': 1.1, 'b': 0})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json()['detail']

    # there must be 2 log entries: 1 for the exception and 1 for the request
    text = capsys.readouterr().err
    position = text.index('\n}\n{\n')

    # test validation log
    validation_log = json.loads(text[: position + 2])
    assert failed_validation_log_fields <= set(validation_log.keys())
    assert 'exception' not in validation_log
    assert validation_log['level'] == 'INFO'
    assert detail == validation_log['detail']

    # test request_log
    request_log = json.loads(text[position + 3 :])
    assert request_log_fields <= set(request_log.keys())
    assert request_log['level'] == 'INFO'
    assert 'exception' not in request_log


async def test_logging_500_exception(
    logging_client: AsyncClient, capsys: CaptureFixture
) -> None:
    """
    Test the log message of a unhandled exception.
    """
    with patch(
        '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
    ):  # prevents highlighting
        response = await logging_client.get('/divide', params={'a': 1, 'b': 0})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.text == 'Internal Server Error'

    log = json.loads(capsys.readouterr().err)
    assert exception_log_fields <= set(log.keys())
    assert log['level'] == 'ERROR'


async def test_logging_http_exception(logging_client: AsyncClient, capsys: CaptureFixture
) -> None:
    for code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
        status.HTTP_405_METHOD_NOT_ALLOWED,
        status.HTTP_409_CONFLICT,
        status.HTTP_429_TOO_MANY_REQUESTS,
    ):
        with patch(
            '{{cookiecutter.project_slug}}.logging.highlight', side_effect=lambda x, y, z: x
        ):  # prevents highlighting
            response = await logging_client.get('/http_exception', params={'code': code})
        assert response.status_code == code
        log = json.loads(capsys.readouterr().err)
        assert request_log_fields <= set(log.keys())
        assert 'exception' not in log
        assert log['level'] == 'INFO'
