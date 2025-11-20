#!/usr/bin/env bash

set -xuo pipefail

cp sample.env .env
rm alembic/versions/empty.txt  # empty.txt was used to keep the alembic folder in version control
uv sync --no-install-project
uv run make format

commit_message="Initial project structure based on https://github.com/andredias/perfect_python_project/tree/fastapi-complete"

if [ "{{cookiecutter.version_control}}" == "hg" ]; then
    hg init .
    hg add
    hg commit -m "$commit_message"
else
    mv .hgignore .gitignore
    git init .
    git add -A .
    git commit -m "$commit_message"
fi

make install_hooks

# initial migration for alembic
docker compose up -d db
sleep 5
uv run alembic revision --autogenerate -m "Initial migration"
docker compose down

# use a separated commit for the initial migration
# so it can be easily reverted if needed
uv run make format
if [ "{{cookiecutter.version_control}}" == "hg" ]; then
    hg commit -Am 'Initial alembic migration'
else
    git commit -am 'Initial alembic migration'
fi
