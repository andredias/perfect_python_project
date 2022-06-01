#!/usr/bin/env python

from subprocess import check_call
from time import sleep

from httpx import get


def run_smoke_test() -> None:
    # fmt: off
    check_call(
        [
            'docker-compose',
            '-f', 'docker-compose.yml',
            '-f', 'docker-compose.smoke_test.yml',
            'up', '-d',
        ]
    )
    # fmt: on
    sleep(2)
    try:
        result = get('http://localhost:5000/hello')
        assert result.status_code == 200
        assert result.json() == {'message': 'Hello World'}
        print('Smoke test passed!')
    finally:
        # fmt: off
        check_call(
            [
                'docker-compose',
                '-f', 'docker-compose.yml',
                '-f', 'docker-compose.smoke_test.yml',
                'down',
            ]
        )
        # fmt: on


if __name__ == '__main__':
    run_smoke_test()
