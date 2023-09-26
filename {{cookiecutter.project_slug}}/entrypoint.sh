#!/bin/bash
set -euo pipefail

if [ "$ENV" != 'production' ]; then
    # ref: https://pythonspeed.com/articles/schema-migrations-server-startup/
    python migrate_database.py
    exec hypercorn --reload --root-path=/api --config=hypercorn.toml {{cookiecutter.project_slug}}.main:app
fi

exec hypercorn --root-path=/api --config=hypercorn.toml {{cookiecutter.project_slug}}.main:app
