import logging

from fastapi import FastAPI
from pytest import LogCaptureFixture


def test_intercept_standard_logging_messages(app: FastAPI, caplog: LogCaptureFixture) -> None:
    """
    Test if loguru intercepts standard logging messages
    """
    caplog.set_level(logging.DEBUG)
    logging.debug('Debug message')
    records = caplog.records
    assert records[0].levelname == 'DEBUG'
    assert records[0].message == 'Debug message'
