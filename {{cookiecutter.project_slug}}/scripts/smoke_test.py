#!/usr/bin/env python

from subprocess import check_call
from time import sleep

from httpx import get


def run_smoke_test() -> None:
    check_call(
        [
            'docker-compose',
            '-f',
            'docker-compose.yml',
            '-f',
            'docker-compose.smoke_test.yml',
            'up',
            '-d',
        ]
    )
    sleep(2)
    try:
        result = get('http://localhost:5000/hello')
        assert result.status_code == 200
        assert result.json() == {'Hello': 'World'}
        print('Smoke test passed!')
    finally:
        check_call(
            [
                'docker-compose',
                '-f',
                'docker-compose.yml',
                '-f',
                'docker-compose.smoke_test.yml',
                'down',
            ]
        )


if __name__ == '__main__':
    run_smoke_test()
