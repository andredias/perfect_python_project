#!/bin/bash
set -eox pipefail

if [ "$ENV" != 'production' ]; then
    exec hypercorn --reload --worker-class={{cookiecutter.worker_class}} --bind=0.0.0.0:5000 \
                   --error-logfile=- --root-path /api \
                   {{cookiecutter.project_slug}}.main:app
else
    exec hypercorn --worker-class={{cookiecutter.worker_class}} --bind=0.0.0.0:5000 --error-logfile=- \
                   --error-logfile=- --root-path /api \
                   {{cookiecutter.project_slug}}.main:app
fi
