#!/bin/bash
set -eoux pipefail

if [ "$ENV" != 'production' ]; then
    # ref: https://pythonspeed.com/articles/schema-migrations-server-startup/
    python migrate_database.py
    exec hypercorn --reload --worker-class={{cookiecutter.worker_class}} --bind=0.0.0.0:5000 \
                   --error-logfile=- --root-path /api \
                   {{cookiecutter.project_slug}}.main:app
else
    exec hypercorn --worker-class={{cookiecutter.worker_class}} --bind=0.0.0.0:5000 --error-logfile=- \
                   --error-logfile=- --root-path /api \
                   {{cookiecutter.project_slug}}.main:app
fi
