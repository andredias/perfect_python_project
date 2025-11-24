#!/bin/bash
set -eoux pipefail

if [ "$ENV" != 'production' ]; then
    # ref: https://pythonspeed.com/articles/schema-migrations-server-startup/
    python migrate_database.py
    exec granian --reload --loop {{cookiecutter.worker_class}} --host 0.0.0.0 --port 5000 \
                 --url-path-prefix /api --interface asgi {{cookiecutter.project_slug}}.main:app
else
    exec granian --loop {{cookiecutter.worker_class}} --host 0.0.0.0 --port 5000 \
                 --url-path-prefix /api --interface asgi {{cookiecutter.project_slug}}.main:app
fi
