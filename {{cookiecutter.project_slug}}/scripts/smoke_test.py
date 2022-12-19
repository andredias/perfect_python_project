#!/usr/bin/env python

from subprocess import check_call

from httpx import get
from loguru import logger
from tenacity import RetryError, retry, stop_after_delay, wait_exponential


def init_containers() -> None:
    command = 'docker-compose -f docker-compose.yml -f docker-compose.smoke_test.yml up -d'
    check_call(command.split())


def stop_containers() -> None:
    command = 'docker-compose -f docker-compose.yml -f docker-compose.smoke_test.yml down'
    check_call(command.split())


@retry(stop=stop_after_delay(3), wait=wait_exponential(multiplier=0.2))
def health_check() -> None:
    result = get('http://localhost:5000/hello')
    assert result.status_code == 200
    assert result.json() == {'message': 'Hello World'}
    logger.info('Smoke test passed!')
    return


def run_smoke_test() -> None:
    init_containers()
    try:
        health_check()
    except RetryError:
        logger.error('Not working')
    finally:
        stop_containers()


if __name__ == '__main__':
    run_smoke_test()
