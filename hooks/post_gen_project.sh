#!/usr/bin/env bash

set -xuo pipefail

poetry env use {{cookiecutter.python_version}}
poetry lock --no-update
poetry install
poetry run make format

commit_message="Initial project structure based on https://github.com/andredias/perfect_python_project/tree/master"

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
