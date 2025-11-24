#!/bin/bash
set -eox pipefail

if [ "$ENV" != 'production' ]; then
    exec granian --reload --loop {{cookiecutter.worker_class}} --host 0.0.0.0 --port 5000 \
                 --interface asgi {{cookiecutter.project_slug}}.main:app
else
    exec granian --loop {{cookiecutter.worker_class}} --host 0.0.0.0 --port 5000 \
                 --interface asgi {{cookiecutter.project_slug}}.main:app
fi
