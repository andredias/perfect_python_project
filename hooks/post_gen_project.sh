#!/bin/bash

poetry update
poetry run make format

if [ "{{cookiecutter.version_control}}" == "hg" ]; then
    hg init .
    if [ -n "{{cookiecutter.github_respository_url}}" ]; then
        echo '[paths]
default = {{cookiecutter.github_respository_url}}
' > .hg/hgrc
    fi
    hg add
    hg commit -m 'Initial project structure'
else
    mv .hgignore .gitignore
    git init .
    if [ -n "{{cookiecutter.github_respository_url}}" ]; then
        git remote add origin {{cookiecutter.github_respository_url}}
    fi
    git add -A .
    git commit -m 'Initial project structure'
fi

poetry run make install_hooks
