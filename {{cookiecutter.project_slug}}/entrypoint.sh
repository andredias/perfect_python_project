#!/bin/bash
set -euo pipefail

if [ "${ENV:-production}" != 'production' ]; then
    python migrate_database.py
fi

exec hypercorn --config=hypercorn.toml {{cookiecutter.project_slug}}.main:app
