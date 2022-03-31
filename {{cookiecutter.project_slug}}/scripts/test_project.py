#!/usr/bin/env python

import os
from subprocess import check_call


def run_tests() -> None:
    os.environ['ENV'] = 'testing'
    check_call(['docker-compose', 'up', '-d'])
    try:
        check_call(
            [
                'pytest',
                '-x',
                '--cov-report=term-missing',
                '--cov-report=html',
                '--cov-branch',
                '--cov={{cookiecutter.project_slug}}',
            ]
        )
    finally:
        check_call(['docker-compose', 'down'])


if __name__ == '__main__':
    run_tests()
