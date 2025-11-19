#!/usr/bin/env bash

set -xuo pipefail

uv sync --no-install-project
uv run make format

commit_message="Initial project structure based on https://github.com/andredias/perfect_python_project/tree/fastapi-minimum"

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
